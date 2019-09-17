#ifndef _ADF_UART_H_
#define _ADF_UART_H_

#include <drivers/gpio/adi_gpio.h>
#include <drivers/uart/adi_uart.h>

void UARTCallback(void* pAppHandle, uint32_t nEvent, void* pArg);
#define UART_CMD_HEADER_NUM_BYTES 6
typedef struct _UartCmd {
    uint16_t cmd_function;    // Last command received
    uint16_t cmd_length;      // Last command argument length
    uint16_t cmd_crc;         // CRC of function + (optional) payload
    bool     header_received; // Received length, now get command
} uartcmd_t;                  /* as much we want*/
/* If DMA mode is enabled */
#if (ADI_UART_CFG_ENABLE_DMA_SUPPORT == 1)
/* and if the DMA is not enable in the adi_uart_Open function */
#if (ADI_UART_CFG_ENABLE_DMA == 0)
#define ENABLE_DMA_MODE
#endif
#endif

/* Memory required by the driver for DMA mode of operation */
#define ADI_UART_MEMORY_SIZE (ADI_UART_BIDIR_MEMORY_SIZE)

#define PRINT_REPORT
#define SIZE_OF_TX_BUFFER 6144
#define SIZE_OF_RX_BUFFER 2048

/* UART device number. There are 2 devices, so this can be 0 or 1. */
#define UART_DEVICE_NUM 0u

/* basic UART functions */
ADI_UART_RESULT adf_uart_init(void);
void            adf_uart_uninit(void);
void            adf_uart_write(uint32_t size, uint8_t* buffer);
void            adf_uart_read(uint32_t size, uint8_t* buffer);
void            adf_uart_write_byte(uint8_t byte);
void            adf_uart_write_word(uint32_t word);
void            adf_uart_read_byte(uint8_t* byte);
uint32_t        adf_uart_read_word(void);
void            adf_uart_write_buffer(uint32_t buffer_size);

#endif //_ADF_UART_H_
