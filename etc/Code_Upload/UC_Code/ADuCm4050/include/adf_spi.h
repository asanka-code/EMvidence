#ifndef _ADF_SPI_H_
#define _ADF_SPI_H_

#include <drivers/gpio/adi_gpio.h>
#include <drivers/pwr/adi_pwr.h>
#include <drivers/spi/adi_spi.h>

#include "hardware_platform.h"

#define ADF_SPI_DEVICE_NUM SENSOR_SPI_NUM
#define ADF_SPI_CSN SENSOR_SPI_CSN

#define ADF_SPI_CLK_FREQ 3000000

/** define size of data buffers, DMA max size is 255 */
#define ADF_SPI_BUFFER_SIZE 2048u

ADI_SPI_RESULT adf_spi_init(ADI_SPI_HANDLE* const phDevice, void* pDevMemory);
ADI_SPI_RESULT adf_spi_uninit(void);
ADI_SPI_RESULT adf_spi_transaction(const uint8_t* txbuf, uint8_t* rxbuf, uint32_t length);

#endif //_ADF_SPI_H_
