/**
 * Functions to read and write to the glue uC via UART, and functions for sensor control via UART
 */

/** @addtogroup UART_PC_Interface
 * @{
 */

#include "adf_timers.h"
#include "adf_uart.h"
#include "adi_uart_config.h"
#include "drivers/uart/adi_uart.h"
#include "statemachine_gui.h"
#include <stdbool.h>

/* Global State Machine */
extern gStateMachine_t globalSM;

// Timeout flag used by Timers
// extern bool_t bTimeOutFlag;

/* Handle for UART device */
extern ADI_UART_HANDLE uartDevice;

/* Buffers for UART driver */
extern uint8_t uart_tx_buffer[SIZE_OF_TX_BUFFER];
extern uint8_t uart_rx_buffer[SIZE_OF_RX_BUFFER];

uartcmd_t uartCmd;

void UARTCallback(void* pAppHandle, uint32_t nEvent, void* pArg) {
    switch (nEvent) {
        case ADI_UART_EVENT_TX_BUFFER_PROCESSED: break;
        case ADI_UART_EVENT_RX_BUFFER_PROCESSED:
            if (!globalSM.cmd_next) {
                if (!uartCmd.header_received) { // Get the header (length + cmd)
                    uartCmd.cmd_length   = (uart_rx_buffer[0] << 8) + uart_rx_buffer[1] - UART_CMD_HEADER_NUM_BYTES;
                    uartCmd.cmd_crc      = (uart_rx_buffer[2] << 8) + uart_rx_buffer[3];
                    uartCmd.cmd_function = (uart_rx_buffer[4] << 8) + uart_rx_buffer[5];

                    if (uartCmd.cmd_length > 0) { // Get extra data if we need it
                        // timer_start(0, 10 * uartCmd.cmd_length); // Start a timer
                        uartCmd.header_received = true;
                        adi_uart_SubmitRxBuffer(uartDevice, uart_rx_buffer, uartCmd.cmd_length, false);
                    } else { // If no extra data to be received, get ready to receiver header again
                        uartCmd.header_received = false;
                        globalSM.cmd_next       = uartCmd.cmd_function;
                        // Re-issue search for new command
                        adi_uart_SubmitRxBuffer(uartDevice, uart_rx_buffer, UART_CMD_HEADER_NUM_BYTES, false);
                    }
                } else { // Get the data after the header
                    uartCmd.header_received = false;
                    globalSM.cmd_next       = uartCmd.cmd_function;
                    // Re-issue search for new command
                    adi_uart_SubmitRxBuffer(uartDevice, uart_rx_buffer, UART_CMD_HEADER_NUM_BYTES, false);
                }
            }
            break;
        case ADI_UART_EVENT_AUTOBAUD_COMPLETE: break;
    }
    /* return */
}

/**
 * @brief Initializes the UART driver. Call this function before using any of the functions in this file.
 */
ADI_UART_RESULT adf_uart_init(void) {

    ADI_UART_RESULT eUartResult = ADI_UART_SUCCESS;

    /*
// Open the UART device. Data transfer is bidirectional with NORMAL mode by default.
if ((eUartResult = adi_uart_Open(UART_DEVICE_NUM, ADI_UART_DIR_BIDIRECTION, UartDeviceMem, ADI_UART_MEMORY_SIZE,
&uartDevice)) != ADI_UART_SUCCESS) { return eUartResult;
}

// Configure  UART device with NO-PARITY, ONE STOP BIT and 8bit word length.
if ((eUartResult = adi_uart_SetConfiguration(uartDevice, ADI_UART_NO_PARITY, ADI_UART_ONE_STOPBIT,
ADI_UART_WORDLEN_8BITS)) != ADI_UART_SUCCESS) { return eUartResult;
}

// Baud rate div values are calcuated for PCLK 26Mhz. Please use the host utility UartDivCalculator.exe provided with
the installer" if ((eUartResult = adi_uart_ConfigBaudRate(uartDevice, UART_DIV_C, UART_DIV_M, UART_DIV_N, UART_OSR)) !=
ADI_UART_SUCCESS) { return eUartResult;
}

//Register callback
if ((eUartResult = adi_uart_RegisterCallback(uartDevice, UARTCallback, uartDevice)) != ADI_UART_SUCCESS) {
    return eUartResult;
}

if ((eUartResult = adi_uart_SubmitRxBuffer(uartDevice, uart_rx_buffer, UART_CMD_HEADER_NUM_BYTES, false))!=
ADI_UART_SUCCESS) { return eUartResult;
}


    */
    return eUartResult;
}

/**
 * @brief Submit all data in the buffer.
 * @param[in] size number of bytes to be submitted
 * @param[in] buffer data to be submitted
 */
void adf_uart_write(uint32_t size, uint8_t* buffer) {
    if (size > SIZE_OF_TX_BUFFER)
        return;
    memcpy(uart_tx_buffer, buffer, size);
    adi_uart_SubmitTxBuffer(uartDevice, uart_tx_buffer, size, false);
}

/**
 * @brief Read a number of bytes.
 * @param[in] size number of bytes to be read
 * @param[out] buffer read buffer
 */
void adf_uart_read(uint32_t size, uint8_t* buffer) {
    uint32_t pHwError;
    adi_uart_Read(uartDevice, buffer, size, false, &pHwError);
}

/**
 * @brief Read 4 bytes from the UART and return as a word (MSB first)
 */
uint32_t adf_uart_read_word(void) {
    uint8_t temp[4];
    adf_uart_read(4, temp);
    return temp[0] + (temp[1] << 8) + (temp[2] << 16) + (temp[3] << 24);
}

/**
 * @brief Write a single byte via UART.
 * @param[in] byte byte to be written
 */
void adf_uart_write_byte(uint8_t byte) {
    uart_tx_buffer[0] = byte;
    adi_uart_SubmitTxBuffer(uartDevice, uart_tx_buffer, 1, false);
}

/**
 * @brief Write a word via UAR (MSVB first)
 * @param[in] word byte to be written
 */
void adf_uart_write_word(uint32_t word) {

    uart_tx_buffer[0] = (word >> 24) & 0xFF;
    uart_tx_buffer[1] = (word >> 16) & 0xFF;
    uart_tx_buffer[2] = (word >> 8) & 0xFF;
    uart_tx_buffer[3] = (word >> 0) & 0xFF;

    adi_uart_SubmitTxBuffer(uartDevice, uart_tx_buffer, 4, false);
}

/**
 * @brief Read a single byte via UART.
 * @param[out] byte data pointer
 */
void adf_uart_read_byte(uint8_t* byte) { adf_uart_read(1, byte); }

/**
 * @brief Submit exisiting data in the tx buffer.
 * @param[in] buffer_size number of bytes to be submitted
 */
void adf_uart_write_buffer(uint32_t buffer_size) { adi_uart_SubmitTxBuffer(uartDevice, uart_tx_buffer, buffer_size, false); }

/** @} */ /* End of group UART PC Interface */
