/**
 * Functions to read and write to the glue uC via UART, and functions for radio control from the GUI
 */

/** @addtogroup UART_PC_Interface
 * @{
 */

#include <stdbool.h>

#include "include/adf_timers.h"
#include "include/adf_uart.h"
#include "include/hardware_platform.h"
#include "include/leds.h"
#include "include/map.h"
#include "include/statemachine_gui.h"
#include "include/uart_buffer.h"
#include "include/uctest/uc_calculations.h"
#include "include/uctest/uc_loops.h"
#include "include/uctest/uc_uecc.h"
#include "interface/interface.h"
#include "interface/interface_uctest.h"

extern gStateMachine_t globalSM;
extern bool            bTimeOutFlag0;

extern uartcmd_t uartCmd;
extern uint8_t   scratch_buffer[SIZE_OF_SCRATCH_BUFFER];
extern uint8_t   uart_rx_buffer[SIZE_OF_RX_BUFFER];

// Timers
extern bool bTimeOutFlag0;

// UC Test
map_void_t map_commands;     // global map
typedef void (*TFUNC)(void); // Function pointer definition

/*
 * @brief Process a command received from the PC using SM info
 */
void uctest_process_command(void) {

    void* call_func = map_get(&map_commands, globalSM.cmd_current);
    if (call_func != NULL) {
        // Unset error bit since we have a calid command
        globalSM.errors_b.cmd_not_found = 0;
        // All commands have repeat and duration values
        const uint16_t duration      = uart_rx_buffer[1] + (uart_rx_buffer[0] << 8); // ms
        uint16_t       repeat        = uart_rx_buffer[3] + (uart_rx_buffer[2] << 8); // default: 1
        TFUNC          test_function = (TFUNC)*map_get(&map_commands, globalSM.cmd_current);

        // If duration specified set up and clean up timers
        if (duration > 0) {
            timer_start_ms(ADI_TMR_DEVICE_GP0, duration);
        }

        if (repeat == 0) {
            // \TODO exit loop if another UART commadn changed
            // If repeat is 0, loop forever or until timeout occurs
            while (true) {
                if (bTimeOutFlag0) {
                    break;
                }
                (*test_function)(); // Run the command
            }
        } else {
            // Repeat for the specified number of times
            while (repeat--) {
                if (bTimeOutFlag0) {
                    break;
                }
                (*test_function)(); // Run the command
            }
        }

        // If duration specified set up and clean up timers
        if (duration > 0) {
            timer_stop(ADI_TMR_DEVICE_GP0);
        }
    } else { // Command not found
        globalSM.errors_b.cmd_not_found = 1;
    };
}

void uctest_setup_commands_map() {
    // Set up Function map
    map_init(&map_commands);
    // uc_loops_function_table
    map_set(&map_commands, 0x1001, &simple_loop);
    map_set(&map_commands, 0x1002, &simple_loop_2);
    map_set(&map_commands, 0x1003, &simple_loop_3);
    map_set(&map_commands, 0x1004, &simple_loop_4);
    map_set(&map_commands, 0x1005, &simple_loop_5);
    map_set(&map_commands, 0x1006, &simple_loop_6);
    map_set(&map_commands, 0x1007, &simple_loop_7);
    map_set(&map_commands, 0x1008, &simple_loop_8);
    map_set(&map_commands, 0x1009, &simple_loop_9);
    map_set(&map_commands, 0x1009, &simple_loop_9);
    map_set(&map_commands, 0x100A, &simple_loop_10);
    // Calculations
    map_set(&map_commands, 0x2001, &calc_additions);
    map_set(&map_commands, 0x2002, &calc_subtractions);
    map_set(&map_commands, 0x2003, &calc_float_mult);
    // uECC
    map_set(&map_commands, 0x3001, &uecc_make_key);
    map_set(&map_commands, 0x3002, &uecc_sign);
    map_set(&map_commands, 0x3003, &uecc_verify);
}

/** @} */ /* End of group UART_PC_Interface */
