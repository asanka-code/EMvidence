/**
 * Functions to read and write to the glue uC via UART, and functions for sensor control from the GUI
 */

/** @addtogroup UART_PC_Interface
 * @{
 */

#include "adf_uart.h"
#include "interface/interface.h"
#include "interface/interface_uctest.h"
#include <stdbool.h>
#include <stdio.h>


#include "adf_timers.h"
#include "crc.h"
#include "uart_buffer.h"

#include "adf_spi.h"
#include "statemachine_gui.h"

extern gStateMachine_t globalSM;

extern uint8_t   uart_rx_buffer[SIZE_OF_RX_BUFFER];
extern uartcmd_t uartCmd;
extern uint8_t   scratch_buffer[SIZE_OF_SCRATCH_BUFFER];
extern uint8_t   spi_buffer_rx[ADF_SPI_BUFFER_SIZE];

/*
 * @brief Process a command received from the PC using SM info
 */
void process_command(void) {

    ADI_GPIO_PORT port;
    ADI_GPIO_DATA pin;
    uint16_t      gpio_data;

    // Set state
    globalSM.errors_b.checksum = 0;
    globalSM.cmd_current       = globalSM.cmd_next;

    // Set up response in buffer
    return_buffer_clear(); // Return Buffer
    return_buffer_add_command(globalSM.cmd_current);

    // Check command CRC, skip processing if invalid
    if (!check_command()) {
        globalSM.errors_b.checksum = 1;
    } else {

        switch (globalSM.cmd_current) {
            /**
             * @brief Return the Compile Date and Version info
             */
            case cmd_get_fw_info: {
                return_buffer_add_byte((uint8_t)BUILD_YEAR);
                return_buffer_add_byte((uint8_t)BUILD_MONTH);
                return_buffer_add_byte((uint8_t)BUILD_DAY);
                return_buffer_add_byte((uint8_t)BUILD_VERSION);

            } break;

            /**
             *@brief Flash the LEDs on the adapter board
             */
            case cmd_flash_LEDs: {
                // leds_flash();
                return_buffer_add_byte(0x00);
            } break;

            /**
             * @brief Set output of the LEDs on the adapter board
             */
            case cmd_set_LEDs: {
                // const char led_data = uart_rx_buffer[0];
                // leds_display(uart_rx_buffer[0]);
                return_buffer_add_byte(0x00);
            } break;

            /**
             * @brief Enable/Disable Glue GPIO
             * To be used when cmd_gpio_enable is received from PC.
             * Enables or disables a gpio.
             */
            case cmd_mcu_gpio_enable: {
                port               = (ADI_GPIO_PORT)uart_rx_buffer[0];
                pin                = (ADI_GPIO_DATA)(1 << uart_rx_buffer[1]);
                const bool isInput = uart_rx_buffer[2];
                const bool enable  = uart_rx_buffer[3];

                if (isInput) {
                    adi_gpio_InputEnable(port, pin, enable);
                } else {
                    adi_gpio_OutputEnable(port, pin, enable);
                }

            } break;

            /**
             * @brief Set a Glue GPIO High or Low
             * To be used when cmd_gpio_set is received from PC.
             * Sets the value of an output pin.
             */
            case cmd_mcu_gpio_set: {
                port = (ADI_GPIO_PORT)uart_rx_buffer[0];
                pin  = (ADI_GPIO_DATA)(1 << uart_rx_buffer[1]);
                // const bool value = (bool)uart_rx_buffer[2];

                if ((bool)uart_rx_buffer[2]) {
                    adi_gpio_SetHigh(port, pin);
                } else {
                    adi_gpio_SetLow(port, pin);
                }

            } break;

            /**
             * @brief Return status of Glue GPIO
             * To be used when cmd_gpio_get is received from PC.
             * Gets the value of an input pin.
             */
            case cmd_mcu_gpio_get: {
                port = (ADI_GPIO_PORT)uart_rx_buffer[0];
                pin  = (ADI_GPIO_DATA)(1 << uart_rx_buffer[1]);
                adi_gpio_GetData(port, pin, &gpio_data);
                // const bool gpio_result = (gpio_data >> uart_rx_buffer[1]);
                return_buffer_add_byte((gpio_data >> uart_rx_buffer[1]));
            } break;

            /**
             * @brief Loop back with 2 bytes. Used to check board connectivity.
             * Return 2 bytes received from PC.
             */
            case cmd_loop_back: {
                return_buffer_add_byte(uart_rx_buffer[0]);
                return_buffer_add_byte(uart_rx_buffer[1]);
            } break;

            /**
             * @brief Set the state machine board number
             **/
            case cmd_sm_set_board_id: {
                globalSM.board_id = uart_rx_buffer[1] + (uart_rx_buffer[0] << 8);
                printf("Board ID: %lu\n", globalSM.board_id);
            } break;

            /**
             * @brief Set the state machine board number
             **/
            case cmd_sm_get_board_id: {
                return_buffer_add_2byte(globalSM.board_id);
            } break;

            /**
             * @brief Clear Glue error status
             */
            case cmd_clear_errors: {
                globalSM.errors = 0;
            } break;

            case cmd_utest_timeout: {
                globalSM.errors_b.timeout = 1;
            } break;

            default: {
                globalSM.errors_b.cmd_not_found = 1;
            }
        }
        // Run command for UC test library
        if (globalSM.cmd_current > 0x1000) {
            uctest_process_command();
        }
    }

    // return_buffer_add_word(globalSM.errors);
    return_buffer_add_byte(globalSM.errors);
    return_buffer_send();

    globalSM.cmd_next = 0x00; // Clear the command in memory
}

bool check_command(void) {

    uint8_t cmd_function_array[2] = {0};
    cmd_function_array[0]         = uartCmd.cmd_function >> 8;
    cmd_function_array[1]         = uartCmd.cmd_function & 0xFF;
    const uint16_t crc_function   = crc16(cmd_function_array, 2, 0x0000);
    const uint16_t crc_computed   = crc16(uart_rx_buffer, uartCmd.cmd_length, crc_function);
    if (crc_computed == uartCmd.cmd_crc)
        return true;
    else
        return false;
}

/** @} */ /* End of group UART_PC_Interface */
