/*
 **
 ** Source file generated on November 28, 2017 at 15:57:54.
 **
 ** Copyright (C) 2011-2017 Analog Devices Inc., All Rights Reserved.
 **
 ** This file is generated automatically based upon the options selected in
 ** the Pin Multiplexing configuration editor. Changes to the Pin Multiplexing
 ** configuration should be made by changing the appropriate options rather
 ** than editing this file.
 **
 ** Selected Peripherals
 ** --------------------
 ** SPI2 (CLK, MOSI, MISO, CS_3)
 **
 ** GPIO (unavailable)
 ** ------------------
 ** P1_02, P1_03, P1_04, P2_07
 */

#include "config.h"
#include <stdint.h>
#include <sys/platform.h>

#define UART0_TX_PORTP0_MUX ((uint32_t)((uint32_t)1 << 20))
#define UART0_RX_PORTP0_MUX ((uint32_t)((uint32_t)1 << 22))

#define SPI2_CLK_PORTP1_MUX ((uint16_t)((uint16_t)1 << 4))
#define SPI2_MOSI_PORTP1_MUX ((uint16_t)((uint16_t)1 << 6))
#define SPI2_MISO_PORTP1_MUX ((uint16_t)((uint16_t)1 << 8))
#define SPI2_CS_3_PORTP2_MUX ((uint16_t)((uint16_t)2 << 14))

#define SPI1_CLK_PORTP1_MUX ((uint16_t)((uint16_t)1 << 12))
#define SPI1_MOSI_PORTP1_MUX ((uint16_t)((uint16_t)1 << 14))
#define SPI1_MISO_PORTP1_MUX ((uint32_t)((uint32_t)1 << 16))
#define SPI1_CS_0_PORTP1_MUX ((uint32_t)((uint32_t)1 << 18))

#define I2C0_SCL_PORT0_MUX ((uint16_t)((uint16_t)1 << 8))
#define I2C0_SDA_PORT0_MUX ((uint16_t)((uint16_t)1 << 10))

int32_t adi_initpinmux(void);

/*
 * Initialize the Port Control MUX Registers
 */
int32_t adi_initpinmux(void) {
    /* PORTx_MUX registers */
    *pREG_GPIO0_CFG = UART0_TX_PORTP0_MUX | UART0_RX_PORTP0_MUX;

#if DUAL_BOARD
    *pREG_GPIO1_CFG = SPI1_CLK_PORTP1_MUX | SPI1_MOSI_PORTP1_MUX | SPI1_MISO_PORTP1_MUX | SPI1_CS_0_PORTP1_MUX;
#endif

#if COG4050 || COG3029
    *pREG_GPIO1_CFG = SPI2_CLK_PORTP1_MUX | SPI2_MOSI_PORTP1_MUX | SPI2_MISO_PORTP1_MUX | I2C0_SCL_PORT0_MUX | I2C0_SDA_PORT0_MUX;
    *pREG_GPIO2_CFG = SPI2_CS_3_PORTP2_MUX;
#endif

#if EZ_KIT
    *pREG_GPIO1_CFG = SPI2_CLK_PORTP1_MUX | SPI2_MOSI_PORTP1_MUX | SPI2_MISO_PORTP1_MUX;
    | I2C0_SCL_PORT0_MUX | I2C0_SDA_PORT0_MUX;
    *pREG_GPIO2_CFG = SPI2_CS_3_PORTP2_MUX;
#endif

    return 0;
}
