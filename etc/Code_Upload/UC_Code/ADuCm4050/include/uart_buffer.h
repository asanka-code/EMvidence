#ifndef __UART_BUFFER_H__
#define __UART_BUFFER_H__

#include <stdint.h>

void return_buffer_send(void);
void return_buffer_clear(void);
void return_buffer_add_byte(uint8_t byte);
void return_buffer_add_2byte(uint16_t byte);
void return_buffer_add_word(uint32_t word);

void return_buffer_add_array(uint16_t len, uint8_t *array);
void return_buffer_add_array32(uint16_t len, uint32_t *array);
void return_buffer_add_command(uint16_t cmd);
void return_buffer_status(uint16_t status);

#endif //__UART_BUFFER_H__
