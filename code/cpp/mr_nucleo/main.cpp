#include "hardware.h"
#include "data_handler.h"
#include "pulse_sequences.h"
#include "config.h"
#include "pico/stdlib.h"
#include <stdio.h>
#include <string>

int main() {
    // Initialize stdio for USB output
    stdio_init_all();
    
    printf("MR-CUKLEO: NMR System Initializing...\n");
    
    // Initialize the hardware
    NMRHardware hardware;
    
    // Initialize pulse sequence handler
    PulseSequence pulseSequence(hardware);
    
    // Initialize data handler
    DataHandler dataHandler;
    
    // Wait for USB to connect
    sleep_ms(2000);
    
    printf("Ready for NMR experiments\n");
    printf("Type 'help' for available commands\n");
    
    char cmd[128];
    
    while (true) {
        printf("> ");
        if (scanf("%127s", cmd) > 0) {
            std::string command(cmd);
            
            if (command == "help") {
                printf("Available commands:\n");
                printf("  spin-echo - Run a spin echo experiment\n");
                printf("  adc - Read ADC value\n");
                printf("  polarize <on/off> - Control polarization\n");
                printf("  help - Show this help\n");
                printf("  exit - Exit program\n");
            }
            else if (command == "spin-echo") {
                printf("Running spin echo sequence...\n");
                std::vector<uint16_t> data = pulseSequence.spin_echo();
                printf("Acquisition complete, %zu points\n", data.size());
                dataHandler.save_data(data);
            }
            else if (command == "adc") {
                uint16_t value = hardware.read_adc();
                printf("ADC value: %u\n", value);
            }
            else if (command == "polarize") {
                char state[4];
                scanf("%3s", state);
                std::string stateStr(state);
                if (stateStr == "on") {
                    hardware.set_polarize(true);
                    printf("Polarization ON\n");
                } 
                else if (stateStr == "off") {
                    hardware.set_polarize(false);
                    printf("Polarization OFF\n");
                }
                else {
                    printf("Invalid state. Use 'on' or 'off'\n");
                }
            }
            else if (command == "exit") {
                printf("Exiting...\n");
                break;
            }
            else {
                printf("Unknown command: %s\n", cmd);
            }
        }
        
        // Flush input buffer
        int c;
        while ((c = getchar_timeout_us(0)) != PICO_ERROR_TIMEOUT) {
            // Discard character
        }
    }
    
    return 0;
}
