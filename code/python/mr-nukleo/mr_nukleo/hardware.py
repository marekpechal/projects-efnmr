from machine import Pin, ADC, PWM
import time
from config import Config


class NMRHardware:
    def __init__(self):
        # Initialize pins
        # TODO: Do we need to pull-up/down some of them?
        self.polarize_control = Pin(Config.POLARIZE_CONTROL_PIN, Pin.OUT, value=0)
        self.tx_positive = Pin(Config.TX_POSITIVE_PIN, Pin.OUT, value=0)
        self.tx_negative = Pin(Config.TX_NEGATIVE_PIN, Pin.OUT, value=0)
        self.tx_enable = Pin(Config.TX_ENABLE_PIN, Pin.OUT, value=0)
        self.rx_enable = Pin(Config.RX_ENABLE_PIN, Pin.OUT, value=0)
        self.adc = ADC(Config.ADC_PIN)

        # Ensure safe initial state
        self.set_polarize(0)
        self.switch_to_receive()

    def set_polarize(self, state):
        """Control the polarization coil."""
        self.polarize_control.value(state)

    def turn_off_polarize_adiabatic(self):
        """Turn off polarization coil adiabatically (fancy word for 'slowly')."""
        self.polarize_control.value(0)
        # Current will decay exponentially according to the circuit time constant
        # Allow time for adiabatic field rotation
        time.sleep(0.01)

    def switch_to_transmit(self):
        """Switch to transmit mode."""
        self.rx_enable.value(0)
        time.sleep(0.001)  # Small delay to ensure relays don't switch simultaneously
        self.tx_enable.value(1)

    def switch_to_receive(self):
        """Switch to receive mode."""
        self.tx_enable.value(0)
        self.tx_positive.value(0)
        self.tx_negative.value(0)
        time.sleep(0.001)  # Small delay to ensure relays don't switch simultaneously
        self.rx_enable.value(1)

    def read_adc(self):
        """Read ADC value."""
        return self.adc.read_u16()
