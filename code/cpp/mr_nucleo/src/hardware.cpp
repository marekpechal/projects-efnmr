#include "hardware.h"
#include "pico/time.h"
#include <iostream>

// Simplified Pin and ADC simulation for this example
// In a real implementation, these would interface with hardware
class Pin {
public:
    Pin(int pin, bool is_output, bool initial_state = false) 
        : pin_number(pin), output(is_output), state(initial_state) {
        std::cout << "Pin " << pin_number << " initialized as " 
                  << (output ? "output" : "input") << std::endl;
    }
    
    void value(bool new_state) {
        state = new_state;
        std::cout << "Pin " << pin_number << " set to " << state << std::endl;
    }
    
private:
    int pin_number;
    bool output;
    bool state;
};

class ADC {
public:
    ADC(int pin) : pin_number(pin) {
        std::cout << "ADC initialized on pin " << pin_number << std::endl;
    }
    
    uint16_t read_u16() {
        // Simulate reading an ADC value (random in this case)
        return rand() % 65536;
    }
    
private:
    int pin_number;
};

NMRHardware::NMRHardware() {
    // Initialize pins
    polarize_control = std::make_unique<Pin>(Config::POLARIZE_CONTROL_PIN, true, false);
    tx_positive = std::make_unique<Pin>(Config::TX_POSITIVE_PIN, true, false);
    tx_negative = std::make_unique<Pin>(Config::TX_NEGATIVE_PIN, true, false);
    tx_enable = std::make_unique<Pin>(Config::TX_ENABLE_PIN, true, false);
    rx_enable = std::make_unique<Pin>(Config::RX_ENABLE_PIN, true, false);
    adc = std::make_unique<ADC>(Config::ADC_PIN);
    
    // Ensure safe initial state
    set_polarize(false);
    switch_to_receive();
}

NMRHardware::~NMRHardware() = default;

void NMRHardware::set_polarize(bool state) {
    polarize_control->value(state);
}

void NMRHardware::turn_off_polarize_adiabatic() {
    polarize_control->value(false);
    // Current will decay exponentially according to the circuit time constant
    // Allow time for adiabatic field rotation
    sleep_ms(10);
}

void NMRHardware::switch_to_transmit() {
    rx_enable->value(false);
    sleep_ms(1);  // Small delay to ensure relays don't switch simultaneously
    tx_enable->value(true);
}

void NMRHardware::switch_to_receive() {
    tx_enable->value(false);
    tx_positive->value(false);
    tx_negative->value(false);
    sleep_ms(1);  // Small delay to ensure relays don't switch simultaneously
    rx_enable->value(true);
}

uint16_t NMRHardware::read_adc() {
    return adc->read_u16();
}

void NMRHardware::set_tx_positive(bool state) {
    tx_positive->value(state);
}

void NMRHardware::set_tx_negative(bool state) {
    tx_negative->value(state);
}
