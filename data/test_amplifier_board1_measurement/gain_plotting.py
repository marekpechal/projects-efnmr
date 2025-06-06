import matplotlib.pyplot as plt
import numpy as np
import scipy
import pickle

def get_sine_amp(data, plot=False, fixed_freq=None):
    spec = abs(np.fft.fft(data))**2
    spec[1:] += spec[::-1][:-1]
    spec[0] = 0
    idx = np.argmax(spec[:len(spec)//2])

    if fixed_freq is None:
        def fitf(x, a, b, c, f):
            return a*np.cos(f*x)+b*np.sin(f*x)+c
        fit = scipy.optimize.curve_fit(fitf, np.arange(len(data)), data,
            [0.0, 0.0, 0.0, 2*np.pi*idx/len(data)])
    else:
        def fitf(x, a, b, c):
            return a*np.cos(f*x)+b*np.sin(fixed_freq*x)+c
        fit = scipy.optimize.curve_fit(fitf, np.arange(len(data)), data,
            [0.0, 0.0, 0.0])

    data_fit = fitf(np.arange(len(data)), *fit[0])

    if plot:
        plt.plot(data)
        plt.plot(data_fit)
        plt.show()

    return (
        fit[0][0]-1j*fit[0][1],
        fit[0][3] if fixed_freq is None else fixed_freq
        )

data_all = np.load("data_rx_amp.npz")
data_fine_all = np.load("data_rx_amp_fine.npz")

R1 = 1.013e6
R2 = 100.0
R3 = 0.990e3
R4 = 100.0
gain_in_out = (R2/(R1+R2))*(R4/(R3+R4))

def gain_th(w):
    R1 = 330.0
    R2 = 330.0e3
    R3 = 15.0e3
    R4 = 370.0
    C1 = 10.0e-9
    C2 = 10.0e-9
    R5 = 150.0e3
    R6 = 2.0e3
    R7 = 1.5e3
    R8 = 15.0e3
    Gbp = -1j*w*C1*R5/R3/(1/R3+1/R4+1j*w*C1+1j*w*C2*(1+1j*w*C1*R5))
    return (1+R2/R1)*Gbp*(-R8/R7)


gains = []
for idx in range(len(data_all["data"])):
    print(data_all["frequencies"][idx])
    v1, f = get_sine_amp(data_all["data"][idx][:-1, 0])
    v2, _ = get_sine_amp(data_all["data"][idx][:-1, 1], fixed_freq=f)
    gain = v2/v1/gain_in_out
    gains.append(gain)
gains = np.array(gains)

gains_fine = []
for idx in range(len(data_fine_all["data"])):
    print(data_fine_all["frequencies"][idx])
    v1, f = get_sine_amp(data_fine_all["data"][idx][:-1, 0])
    v2, _ = get_sine_amp(data_fine_all["data"][idx][:-1, 1], fixed_freq=f)
    gain = v2/v1/gain_in_out
    gains_fine.append(gain)
gains_fine = np.array(gains_fine)


interp_data = np.array(sorted(
    list(zip(data_all["frequencies"], gains)) +
    list(zip(data_fine_all["frequencies"], gains_fine)),
    key=lambda p:p[0]))
with open("gain_interpf_log10log10.pickle", "wb") as f:
    pickle.dump(scipy.interpolate.interp1d(
        np.log10(abs(interp_data[:, 0])),
        np.log10(abs(interp_data[:, 1])),
        kind="linear"
        ), f)

plt.figure(figsize=(8, 4))

plt.subplot(2, 2, 1)
plt.loglog(data_all["frequencies"], abs(gains), ".-",
    label="measurement")
plt.loglog(
    data_all["frequencies"],
    [abs(gain_th(2*np.pi*f)) for f in data_all["frequencies"]], "k-",
    label="theory")
plt.grid()
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Voltage gain")

plt.subplot(2, 2, 2)
plt.plot(data_fine_all["frequencies"], abs(gains_fine), ".-",
    label="measurement")
plt.plot(
    data_fine_all["frequencies"],
    [abs(gain_th(2*np.pi*f)) for f in data_fine_all["frequencies"]], "k-",
    label="theory")
plt.grid()
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Voltage gain")

plt.subplot(2, 2, 3)
plt.semilogx(data_all["frequencies"], np.log(gains).imag*180/np.pi, ".-",
    label="measurement")
plt.semilogx(
    data_all["frequencies"],
    [np.log(gain_th(2*np.pi*f)).imag*180/np.pi for f in data_all["frequencies"]], "k-",
    label="theory")
plt.grid()
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Phase [deg]")

plt.subplot(2, 2, 4)
plt.plot(data_fine_all["frequencies"], np.log(gains_fine).imag*180/np.pi, ".-",
    label="measurement")
plt.plot(
    data_fine_all["frequencies"],
    [np.log(gain_th(2*np.pi*f)).imag*180/np.pi for f in data_fine_all["frequencies"]], "k-",
    label="theory")
plt.grid()
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Phase [deg]")

plt.tight_layout()
plt.savefig("fig_gain_measurement_plots.png")
plt.show()
