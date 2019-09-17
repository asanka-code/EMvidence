/**
 * SPI functions for the glue uC and RF transceiver
 */

/** @addtogroup ADF_SPI
 * @{
 */

#include <stdbool.h>
#include <stdint.h>

#include "adf_spi.h"
#include "hardware_platform.h"
#include <drivers/spi/adi_spi.h>

static ADI_SPI_HANDLE* pSpiDevice;

/**
 * Initialize the SPI driver
 */
ADI_SPI_RESULT adf_spi_init(ADI_SPI_HANDLE* const phDevice, void* pDevMemory) {

    ADI_SPI_RESULT eResult = ADI_SPI_SUCCESS;

    pSpiDevice = phDevice;

    /* initialize SPI2 */
    eResult = adi_spi_Open(SENSOR_SPI_NUM, pDevMemory, ADI_SPI_MEMORY_SIZE, pSpiDevice);
    if (eResult)
        return eResult;

    /* set bit rate */
    eResult = adi_spi_SetBitrate(*pSpiDevice, ADF_SPI_CLK_FREQ);
    if (eResult)
        return eResult;

    eResult = adi_spi_SetChipSelect(*pSpiDevice, SENSOR_SPI_CSN);
    if (eResult)
        return eResult;

    eResult = adi_spi_SetMasterMode(*pSpiDevice, true);
    if (eResult)
        return eResult;

    eResult = adi_spi_SetContinuousMode(*pSpiDevice, true);

    return eResult;
}

ADI_SPI_RESULT adf_spi_uninit(void) { return adi_spi_Close(*pSpiDevice); }

/**
 * @brief Perform a SPI transaction.
 * @param txbuf transmitter buffer
 * @param length size of data to be transmitted
 * @param rxbuf reciever buffer
 */
ADI_SPI_RESULT adf_spi_transaction(const uint8_t* txbuf, uint8_t* rxbuf, uint32_t length) {
    ADI_SPI_RESULT eResult = ADI_SPI_SUCCESS;

    ADI_SPI_TRANSCEIVER transceive = {
        .pTransmitter     = (uint8_t*)txbuf,
        .pReceiver        = (uint8_t*)rxbuf,
        .TransmitterBytes = length,
        .ReceiverBytes    = length,
        .nTxIncrement     = 1,
        .nRxIncrement     = 1,
        .bDMA             = false,
        .bRD_CTL          = false,
    };

    eResult = adi_spi_MasterReadWrite(*pSpiDevice, &transceive); // Blocking

    return eResult;
}

/** @} */ /* End of group ADF SPI */
