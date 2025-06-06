import numpy as np
import matplotlib.pyplot as plt
import os
import time
import logging
import scipy

logging.basicConfig(level="INFO")
TMP_FILE = "/root/data.txt"

def exec_rp_cmd(address, rp_cmd, user="root", pw="root"):
    """Execute command on the red pitaya.

    Args:
        address (str): Network address of the red pitaya.
        rp_cmd (str): Command to be executed.
        user (str, optional): User name for login. Defaults to `root`.
        pw (str, optional): Password for login. Defaults to `root`.
    """

    logging.info(f"executing command: {rp_cmd}")
    cmd = f'plink -batch -pw {pw} {user}@{address} "{rp_cmd}"'
    os.system(cmd)

def get_rp_file(address, rp_path, dst_path, user="root", pw="root"):
    """Copy file from the red pitaya.

    Args:
        address (str): Network address of the red pitaya.
        rp_path (str): File path on the red pitaya.
        dst_path (str): Destination path.
        user (str, optional): User name for login. Defaults to `root`.
        pw (str, optional): Password for login. Defaults to `root`.
    """

    logging.info(f"copying file: {rp_path} > {dst_path}")
    cmd = f"pscp -batch -pw {pw} {user}@{address}:{rp_path} {dst_path}"
    os.system(cmd)

def delete_rp_file(address, rp_path, user="root", pw="root"):
    """Delete file from the red pitaya.

    Args:
        address (str): Network address of the red pitaya.
        rp_path (str): File path on the red pitaya.
        user (str, optional): User name for login. Defaults to `root`.
        pw (str, optional): Password for login. Defaults to `root`.
    """

    exec_rp_cmd(address, f"rm {rp_path}", user=user, pw=pw)

def init(address, user="root", pw="root"):
    """Initialize overlay to upload the required FPGA BIN file.

    Args:
        address (str): Network address of the red pitaya.
        user (str, optional): User name for login. Defaults to `root`.
        pw (str, optional): Password for login. Defaults to `root`.
    """

    exec_rp_cmd(address,
        "bash /opt/redpitaya/sbin/overlay.sh v0.94",
        user=user,
        pw=pw)

def generate_sine(address, channel, vpp, frequency, user="root", pw="root"):
    """Generate sine wave on one of the red pitaya's output channels.

    Args:
        address (str): Network address of the red pitaya.
        channel (int): Channel number 1 or 2.
        vpp (float): Sine wave peak-to-peak amplitude in volts.
        frequency (float): Sine wave frequency in hertz.
        user (str, optional): User name for login. Defaults to `root`.
        pw (str, optional): Password for login. Defaults to `root`.
    """

    exec_rp_cmd(address,
        f"/opt/redpitaya/bin/generate {channel} {vpp} {frequency} sine",
        user=user,
        pw=pw)

def acquire(address, n_samples, decimation_factor, user="root", pw="root"):
    """Acquire data from the red pitaya's input channels.

    Args:
        address (str): Network address of the red pitaya.
        n_samples (int): Number of samples to record.
        decimation_factor (int): Decimation factor.
        user (str, optional): User name for login. Defaults to `root`.
        pw (str, optional): Password for login. Defaults to `root`.

    The data are saved locally on the red pitaya in a temporary file.
    """

    exec_rp_cmd(address,
        f"/opt/redpitaya/bin/acquire -o -1 hv -2 hv " +\
            f"{n_samples} {decimation_factor} >> {TMP_FILE}",
        user=user,
        pw=pw)

def get_data(address, user="root", pw="root"):
    """Grab recorded data from the red pitaya.

    Args:
        address (str): Network address of the red pitaya.
        user (str, optional): User name for login. Defaults to `root`.
        pw (str, optional): Password for login. Defaults to `root`.

    Returns:
        numpy.array: Float array of shape (n_samples, 2).
    """
    local_tmp_file = "data.txt"
    get_rp_file(address, TMP_FILE, local_tmp_file, user=user, pw=pw)
    delete_rp_file(address, TMP_FILE, user=user, pw=pw)
    with open(local_tmp_file, "r") as f:
        data = np.array([
            [float(s) for s in line.split(" ") if s]
            for line in f])
    os.remove(local_tmp_file)
    return data

if __name__ == "__main__":
    address = "rp-f00286"
    channel = 1
    vpp = 2.0
    n_samples = 16384
    decimation_factor = 2048
    # frequencies = [
    #     round(f)
    #     for f in np.exp(np.linspace(np.log(10.0), np.log(10000.0), 121))]
    frequencies = [
        round(f)
        for f in np.linspace(2000.0, 2500.0, 101)]

    init(address)
    data_all = []
    for frequency in frequencies:
        logging.info(f"measuring with frequency {frequency} Hz")
        generate_sine(address, channel, vpp, frequency)
        time.sleep(0.2)
        acquire(address, n_samples, decimation_factor)
        data = get_data(address)
        data_all.append(data)

    data_all = np.array(data_all)
    np.savez("data_rx_amp_finest.npz",
        data=data_all,
        frequencies=frequencies)
