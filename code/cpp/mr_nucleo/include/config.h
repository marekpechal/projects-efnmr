#pragma once

namespace Config {
    // Pin configurations
    constexpr int POLARIZE_CONTROL_PIN = 2;  // Example pin number, adjust as needed
    constexpr int TX_POSITIVE_PIN = 3;
    constexpr int TX_NEGATIVE_PIN = 4;
    constexpr int TX_ENABLE_PIN = 5;
    constexpr int RX_ENABLE_PIN = 6;
    constexpr int ADC_PIN = 26;  // Assuming ADC0 on Pico
    
    // Timing configurations
    constexpr float POLARIZE_TIME = 1.0;  // seconds
    constexpr float DEAD_TIME = 0.001;    // seconds
    
    // NMR parameters
    constexpr int NMR_FREQUENCY = 2000;   // Hz
    constexpr int SAMPLE_RATE = 10000;    // samples per second
    
    // Buffer size for data acquisition
    constexpr int BUFFER_SIZE = 1000;
}