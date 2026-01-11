import time
import array
from config import Config
from hardware import NMRHardware


class PulseSequence:
    def __init__(self, hardware):
        self.hw = hardware
        self.data_buffer = array.array("H", [0] * Config.BUFFER_SIZE)

    def pulse_90_degrees(self, duration_ms):
        """Apply a 90 degree pulse."""
        half_cycle_us = int(500000 / Config.NMR_FREQUENCY)
        num_cycles = int((duration_ms * 1000) / (2 * half_cycle_us))

        self.hw.switch_to_transmit()

        # Generate phase-coherent audio frequency pulse
        for i in range(num_cycles):
            self.hw.tx_positive.value(1)
            self.hw.tx_negative.value(0)
            time.sleep_us(half_cycle_us)
            self.hw.tx_positive.value(0)
            self.hw.tx_negative.value(1)
            time.sleep_us(half_cycle_us)

        self.hw.tx_positive.value(0)
        self.hw.tx_negative.value(0)

        self.hw.switch_to_receive()
        time.sleep(Config.DEAD_TIME)  # switching transients decay

    def pulse_180_degrees(self, duration_ms):
        """Apply a 180 degree pulse (twice the 90 degree pulse)."""
        self.pulse_90_degrees(duration_ms * 2)

    def acquire_data(self, num_points):
        """Acquire NMR signal."""
        interval_us = int(1000000 / Config.SAMPLE_RATE)

        # Acquire data points
        for i in range(min(num_points, len(self.data_buffer))):
            self.data_buffer[i] = self.hw.read_adc()
            time.sleep_us(interval_us)

        return self.data_buffer[:num_points]

    def spin_echo(self, echo_time_ms=10, pulse_90_duration_ms=1.25):
        """Execute a spin-echo pulse sequence."""
        try:
            self.hw.set_polarize(1)
            time.sleep(Config.POLARIZE_TIME)
            self.hw.turn_off_polarize_adiabatic()
            self.pulse_90_degrees(pulse_90_duration_ms)
            time.sleep(echo_time_ms / 2000.0)
            self.pulse_180_degrees(pulse_90_duration_ms)
            time.sleep(echo_time_ms / 2000.0)

            data = self.acquire_data(Config.BUFFER_SIZE)
            return data
        except Exception as e:
            print(f"Error in spin echo sequence: {e}")
            return None

    def cpmg(self, num_echoes=16, echo_time_ms=10, pulse_90_duration_ms=1.25):
        """Execute a Carr-Purcell-Meiboom-Gill sequence."""
        try:
            # Store all echoes
            all_echoes = []
            points_per_echo = Config.BUFFER_SIZE // num_echoes

            self.hw.set_polarize(1)
            time.sleep(Config.POLARIZE_TIME)
            self.hw.turn_off_polarize_adiabatic()

            # x-axis
            self.pulse_90_degrees(pulse_90_duration_ms)

            # Acquisition
            for i in range(num_echoes):
                time.sleep(echo_time_ms / 2000.0)

                # y-axis (phase shifted)
                self.pulse_180_degrees(pulse_90_duration_ms)

                time.sleep(echo_time_ms / 2000.0)

                echo_data = self.acquire_data(points_per_echo)
                all_echoes.append(list(echo_data))

            return all_echoes
        except Exception as e:
            print(f"Error in CPMG sequence: {e}")
            return None
