#include "adf_uart.h"
#include "uart_buffer.h"


extern uint8_t uart_tx_buffer[SIZE_OF_TX_BUFFER];

static uint32_t uart_tx_len;

void return_buffer_send(void) {
    uart_tx_buffer[0] = (uart_tx_len & 0xFF00) >> 8;
    uart_tx_buffer[1] = uart_tx_len & 0xFF;
    adf_uart_write_buffer(uart_tx_len);
}

void return_buffer_clear(void) { uart_tx_len = 4; }

void return_buffer_add_byte(uint8_t byte) {
    uart_tx_buffer[uart_tx_len] = byte;
    uart_tx_len++;
}

void return_buffer_add_2byte(uint16_t word) {
    uart_tx_buffer[uart_tx_len]     = (word >> 8) & 0xFF;
    uart_tx_buffer[uart_tx_len + 1] = (word >> 0) & 0xFF;
    uart_tx_len += 2;
}
void return_buffer_add_word(uint32_t word) {
    uart_tx_buffer[uart_tx_len]     = (word >> 24) & 0xFF;
    uart_tx_buffer[uart_tx_len + 1] = (word >> 16) & 0xFF;
    uart_tx_buffer[uart_tx_len + 2] = (word >> 8) & 0xFF;
    uart_tx_buffer[uart_tx_len + 3] = (word >> 0) & 0xFF;
    uart_tx_len += 4;
}

void return_buffer_add_array(uint16_t len, uint8_t* array) {
    for (uint16_t inc = 0; inc < len; inc++) {
        uart_tx_buffer[uart_tx_len] = array[inc];
        uart_tx_len++;
    }
}

void return_buffer_add_array32(uint16_t len, uint32_t* array) {
    for (uint16_t inc = 0; inc < len; inc++) {
        uart_tx_buffer[uart_tx_len]     = (array[inc] >> 24) & 0xFF;
        uart_tx_buffer[uart_tx_len + 1] = (array[inc] >> 16) & 0xFF;
        uart_tx_buffer[uart_tx_len + 2] = (array[inc] >> 8) & 0xFF;
        uart_tx_buffer[uart_tx_len + 3] = (array[inc] >> 0) & 0xFF;
        uart_tx_len += 4;
    }
}

void return_buffer_add_command(uint16_t cmd) {
    uart_tx_buffer[2] = (cmd & 0xFF00) >> 8;
    uart_tx_buffer[3] = cmd & 0xFF;
}

void return_buffer_status(uint16_t status) {
    return_buffer_add_byte((status >> 8) & 0xFF);
    return_buffer_add_byte(status & 0xFF);
}
