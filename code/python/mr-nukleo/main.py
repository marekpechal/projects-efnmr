# NMR using a RP2350 as controller

import sys
import time
from mr_nukleo.config import Config
from mr_nukleo.hardware import NMRHardware
from mr_nukleo.pulse_sequences import PulseSequence
from mr_nukleo.data_handler import DataHandler

def display_menu():
    """Display the main menu"""
    print("\nEarth's Field NMR on RP2050")
    print("-" * 30)
    print("1. Spin Echo")
    print("2. CPMG Multi-Echo")
    print("3. Configure Parameters")
    print("4. Test Hardware")
    print("5. Exit")
    return input("Select option (1-5): ")

def configure_parameters():
    """Allow user to update configuration parameters"""
    print("\nConfigure Parameters")
    print("-" * 30)
    print("Current settings:")
    print(f"1. SAMPLE_RATE: {Config.SAMPLE_RATE} Hz")
    print(f"2. NMR_FREQUENCY: {Config.NMR_FREQUENCY} Hz")
    print(f"3. POLARIZE_TIME: {Config.POLARIZE_TIME} s")

    choice = input("\nEnter parameter number to change (or 0 to return): ")

    if choice == "1":
        value = input("Enter new SAMPLE_RATE (Hz): ")
        Config.update(SAMPLE_RATE=int(value))
    elif choice == "2":
        value = input("Enter new NMR_FREQUENCY (Hz): ")
        Config.update(NMR_FREQUENCY=int(value))
    elif choice == "3":
        value = input("Enter new POLARIZE_TIME (s): ")
        Config.update(POLARIZE_TIME=float(value))

def test_hardware(hardware):
    """Test hardware components"""
    print("\nHardware Test")
    print("-" * 30)
    print("1. Test Polarize Coil")
    print("2. Test Transmit Circuit")
    print("3. Test Receive Circuit")
    choice = input("Select test (1-3): ")

    if choice == "1":
        print("Turning on polarize coil for 2 seconds...")
        hardware.set_polarize(1)
        time.sleep(2)
        print("Turning off polarize coil...")
        hardware.turn_off_polarize_adiabatic()

    elif choice == "2":
        print("Testing transmit circuit - 10 pulses...")
        hardware.switch_to_transmit()
        for i in range(10):
            hardware.tx_positive.value(1)
            hardware.tx_negative.value(0)
            time.sleep(0.001)
            hardware.tx_positive.value(0)
            hardware.tx_negative.value(1)
            time.sleep(0.001)
        hardware.tx_positive.value(0)
        hardware.tx_negative.value(0)
        hardware.switch_to_receive()

    elif choice == "3":
        print("Testing ADC readings...")
        hardware.switch_to_receive()
        for i in range(5):
            value = hardware.read_adc()
            print(f"ADC reading {i+1}: {value}")
            time.sleep(0.5)

def main():
    try:
        # Initialize system components
        hardware = NMRHardware()
        pulse_seq = PulseSequence(hardware)
        data_handler = DataHandler()

        while True:
            choice = display_menu()

            if choice == "1":
                print("\nRunning Spin Echo sequence...")
                echo_time = float(input("Echo time (ms) [default=10]: ") or 10)
                pulse_duration = float(input("90° pulse duration (ms) [default=1.25]: ") or 1.25)

                data = pulse_seq.spin_echo(echo_time_ms=echo_time, pulse_90_duration_ms=pulse_duration)
                if data:
                    print("Acquisition complete.")
                    data_handler.send_data_serial(data)
                    save = input("Save data? (y/n): ").lower() == 'y'
                    if save:
                        data_handler.save_data(data)

            elif choice == "2":
                print("\nRunning CPMG sequence...")
                num_echoes = int(input("Number of echoes [default=16]: ") or 16)
                echo_time = float(input("Echo time (ms) [default=10]: ") or 10)
                pulse_duration = float(input("90° pulse duration (ms) [default=1.25]: ") or 1.25)

                data = pulse_seq.cpmg(num_echoes=num_echoes, echo_time_ms=echo_time,
                                     pulse_90_duration_ms=pulse_duration)
                if data:
                    print("Acquisition complete.")
                    data_handler.send_data_serial(data)
                    save = input("Save data? (y/n): ").lower() == 'y'
                    if save:
                        data_handler.save_data(data)

            elif choice == "3":
                configure_parameters()

            elif choice == "4":
                test_hardware(hardware)

            elif choice == "5":
                print("Exiting program...")
                hardware.set_polarize(0)  # Ensure polarize is off
                hardware.switch_to_receive()  # Safe state
                sys.exit(0)

            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        # Ensure system is in safe state
        hardware.set_polarize(0)
        hardware.switch_to_receive()
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Try to ensure system is in safe state
        try:
            hardware.set_polarize(0)
            hardware.switch_to_receive()
        except:
            pass

if __name__ == "__main__":
    main()
