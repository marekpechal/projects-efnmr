import matplotlib.pyplot as plt
import numpy as np
import scipy

max_sampling_rate = 125.0e6
decimation_factor = 2048
n_samples = 16384

T = n_samples/(max_sampling_rate/decimation_factor)
df = 1/T

freqs = np.arange(n_samples)*df

data_all = np.load("data_psd_cal_sig.npy")
psd_cal_sig = np.mean([abs(np.fft.fft(wfm[:, 0]))**2 for wfm in data_all],
    axis=0) * (2*T/n_samples**2)

data_all = np.load("data_psd_short.npy")
psd_short = np.mean([abs(np.fft.fft(wfm[:, 0]))**2 for wfm in data_all],
    axis=0) * (2*T/n_samples**2)

data_all = np.load("data_psd_short2.npy")
psd_short2 = np.mean([abs(np.fft.fft(wfm[:, 0]))**2 for wfm in data_all],
    axis=0) * (2*T/n_samples**2)

data_all = np.load("data_psd_amp.npy")
psd_amp = np.mean([abs(np.fft.fft(wfm[:, 0]))**2 for wfm in data_all],
    axis=0) * (2*T/n_samples**2)

print(f"total cal. signal <v^2> = {sum(psd_cal_sig)*df} (should be 0.5)")

plt.figure(figsize=(6, 3))
plt.semilogy(freqs, np.sqrt(psd_amp), label="amplifier output")
# plt.semilogy(freqs, np.sqrt(psd_short2), label="short2")
plt.semilogy(freqs, np.sqrt(psd_short), label="background")
# plt.semilogy(freqs, np.sqrt(psd_amp-psd_short), label="amp (w/o bg)")
plt.legend()
plt.grid()
plt.xlim((0, 12000))
plt.ylim((1e-6, 4e-4))
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD [$\\mathrm{V}/\\sqrt{\\mathrm{Hz}}$]")
plt.tight_layout()
plt.savefig("fig_noise_measurement_rp_plots.png")
plt.show()
