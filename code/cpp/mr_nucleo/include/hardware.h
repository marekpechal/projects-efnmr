#pragma once

#include "config.h"
#include <cstdint>
#include <memory>

class Pin;
class ADC;

class NMRHardware {
public:
    NMRHardware();
    ~NMRHardware();
    
    void set_polarize(bool state);
    void turn_off_polarize_adiabatic();
    void switch_to_transmit();
    void switch_to_receive();
    uint16_t read_adc();    
    void set_tx_positive(bool state);
    void set_tx_negative(bool state);
    
private:
    std::unique_ptr<Pin> polarize_control;
    std::unique_ptr<Pin> tx_positive;
    std::unique_ptr<Pin> tx_negative;
    std::unique_ptr<Pin> tx_enable;
    std::unique_ptr<Pin> rx_enable;
    std::unique_ptr<ADC> adc;
};
