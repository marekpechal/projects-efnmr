"""
Spectrum measured with the RTB2004 at RBW = 10Hz, ac coupling (2 Hz cutoff)
Frequency in Hz, power in dBV
"""

import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
sys.path.insert(-1, "E:\\projects\\EFNMR\\code\\python\\opamp_circuit_analysis")
from opamp_circuit import Circuit, Resistor, Capacitor, IdealOpAmp, \
    IdealVoltageSource, IdealCurrentSource

def predict_noise(frange):
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
    circuit = Circuit()
    circuit.add(Resistor(R1, ["oa1_in_inv", "gnd"], name="R1"))
    circuit.add(Resistor(R2, ["oa1_in_inv", "oa1_out"], name="R2"))
    circuit.add(IdealOpAmp(["oa1_in_noninv", "oa1_in_inv", "oa1_out"], name="OA1"))
    circuit.add(IdealVoltageSource("Vin", ["oa1_in_noninv", "gnd"]))
    circuit.add(Resistor(R3, ["oa1_out", "int1"], name="R3"))
    circuit.add(Resistor(R4, ["int1", "gnd"], name="R4"))
    circuit.add(Capacitor(C1, ["int1", "oa2_in_inv"], name="C1"))
    circuit.add(Capacitor(C2, ["int1", "oa2_out"], name="C2"))
    circuit.add(Resistor(R5, ["oa2_in_inv", "oa2_out"], name="R5"))
    circuit.add(IdealOpAmp(["gnd", "oa2_in_inv", "oa2_out"], name="OA2"))
    circuit.add(Resistor(R6, ["gnd", "oa2_out"], name="R6"))
    circuit.add(Resistor(R7, ["oa2_out", "oa3_in_inv"], name="R7"))
    circuit.add(Resistor(R8, ["oa3_in_inv", "oa3_out"], name="R8"))
    circuit.add(IdealOpAmp(["gnd", "oa3_in_inv", "oa3_out"], name="OA3"))
    circuit.add_noise_sources()

    noiseAmpV = []
    noiseAmpI = []
    noiseRes = []
    for f in frange:
        sol = circuit.solve(2*np.pi*f)
        noiseAmpV.append(abs(sol["Vnoise_OA1"]["oa3_out"])**2
            + abs(sol["Vnoise_OA2"]["oa3_out"])**2
            + abs(sol["Vnoise_OA3"]["oa3_out"])**2)
        noiseAmpI.append(
            abs(sol["Inoise1_OA1"]["oa3_out"])**2
                + abs(sol["Inoise1_OA2"]["oa3_out"])**2
                + abs(sol["Inoise1_OA3"]["oa3_out"])**2 +
            abs(sol["Inoise2_OA1"]["oa3_out"])**2
                + abs(sol["Inoise2_OA2"]["oa3_out"])**2
                + abs(sol["Inoise2_OA3"]["oa3_out"])**2)
        noiseRes.append(sum([c.R*abs(sol[f"Vnoise_{c.name}"]["oa3_out"])**2
            for c in circuit.components if isinstance(c, Resistor)]))
    noiseAmpV = np.array(noiseAmpV)
    noiseAmpI = np.array(noiseAmpI)
    noiseRes = np.array(noiseRes)

    bg = 2.4e-6
    return np.sqrt(
        noiseAmpV*(2.2e-9)**2 +
        noiseAmpI*(5.0e-13)**2 +
        4*1.38e-23*300*noiseRes +
        bg**2)

with open("gain_interpf_log10log10.pickle", "rb") as f:
    gain_log10log10 = pickle.load(f)


def load_psd(filename, RBW=10.0):
    data = []
    with open(filename, "r") as f:
        for line in list(f)[1:]:
            data.append([float(s) for s in line.split(",")])
    data = np.array(data)
    data[:, 1] = np.sqrt(10.0**(data[:, 1]/10)/RBW) # convert to V/sqrt(Hz)
    return data

data_amp = load_psd("data_psd2_amp.csv")
data_bg = load_psd("data_psd2_bg.csv")

plt.figure(figsize=(6, 6))

plt.subplot(2, 1, 1)
plt.semilogy(data_amp[:, 0], data_amp[:, 1], label="amplifier output")
plt.semilogy(data_amp[:, 0], predict_noise(data_amp[:, 0]), "--",
    color="black",
    label="theory")
plt.semilogy(data_bg[:, 0], data_bg[:, 1], label="background")
plt.grid()
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD [$\\mathrm{V}/\\sqrt{\\mathrm{Hz}}$]")
plt.ylim((1e-6, 4e-4))

plt.subplot(2, 1, 2)
mask = np.logical_and(20.0<data_amp[:, 0], data_amp[:, 0]<10000.0)
plt.semilogy(data_amp[mask, 0], [
        data_amp[i, 1]/10**gain_log10log10(np.log10(data_amp[i, 0]))
        for i in np.arange(len(data_amp))[mask]])
plt.grid()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Input-referred PSD [$\\mathrm{V}/\\sqrt{\\mathrm{Hz}}$]")
plt.ylim((7e-10, 5e-8))

plt.tight_layout()
plt.savefig("fig_noise_measurement_plots.png")
plt.show()
