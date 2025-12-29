# Configuration settings for the NMR system
# Mostly adapted from: https://iopscience.iop.org/article/10.1088/0957-0233/21/10/105902/pdf?casa_token=AWc-8OAlQGcAAAAA:wAT60IeW-pmnMYeHheOMp8pbztTdoiybjYJTmstfJI0FGRBpWJFOgXIliolyYJ7_ZwgcsUADAlfaXYVDJrxNsuknxU0
class Config:
    SAMPLE_RATE = 9615  # Hz, as in the original design
    NMR_FREQUENCY = 2000  # Hz, typical proton Larmor frequency in Earth's field
    POLARIZE_TIME = 7  # seconds
    DEAD_TIME = 0.010  # 10 ms, time between pulse and acquisition

    # Pin assignments
    POLARIZE_CONTROL_PIN = 0  # Controls the MOSFETs for polarization coil
    TX_POSITIVE_PIN = 1  # Positive phase for transmitter waveform
    TX_NEGATIVE_PIN = 2  # Negative phase for transmitter waveform
    TX_ENABLE_PIN = 3  # TODO: Controls the transmit relay
    RX_ENABLE_PIN = 4  # TODO: Controls the receive relay
    ADC_PIN = 26  # ADC input for signal acquisition

    # TODO: RP2350
    # - Using C++ we can get 20x faster here

    # Buffer size
    BUFFER_SIZE = 16384

    @classmethod
    def update(cls, **kwargs):
        """Optionally change some the initial parameters."""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
                print(f"Updated {key} to {value}")
            else:
                print(f"Warning: {key} is not a valid configuration parameter")
