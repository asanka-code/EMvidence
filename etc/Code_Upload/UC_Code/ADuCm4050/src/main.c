/*****************************************************************************
 * testUC.c
 *****************************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/platform.h>

#include <drivers/gpio/adi_gpio.h>
#include <drivers/pwr/adi_pwr.h>
#include <drivers/rng/adi_rng.h>
#include <drivers/spi/adi_spi.h>
#include <drivers/uart/adi_uart.h>
#include <drivers/xint/adi_xint.h>

#include "include/adf_spi.h"
#include "include/adf_timers.h"
#include "include/adf_uart.h"
#include "include/common_debug.h"
#include "include/interface/interface.h"
#include "include/interface/interface_uctest.h"
#include "include/leds.h"
#include "include/main.h"
#include "include/random.h"
#include "include/statemachine_gui.h"
#include "system/adi_initialize.h"

/* Handle for the UART device. */
ADI_UART_HANDLE uartDevice;

/* Memory for the UART driver. */
static uint8_t UartDeviceMem[ADI_UART_MEMORY_SIZE];

uint8_t GPIOCallbackMem[ADI_GPIO_MEMORY_SIZE];
// External Interrupt
static uint8_t xintMemory[ADI_XINT_MEMORY_SIZE];

/* RNG Device Handle */
ADI_RNG_HANDLE rngDevice;
/* Memory to handle CRC Device */
static uint8_t RngDevMem[ADI_RNG_MEMORY_SIZE];

// SPI Driver Handle and Memory
// ADI_SPI_HANDLE spiDevice;
// static uint8_t spiDeviceMem[ADI_SPI_MEMORY_SIZE] __attribute__((aligned(2)));

// UART Buffers
__attribute__((section(".uart_buffer_rx"))) uint8_t uart_rx_buffer[SIZE_OF_RX_BUFFER] = {0};
__attribute__((section(".uart_buffer_tx"))) uint8_t uart_tx_buffer[SIZE_OF_TX_BUFFER] = {0};

// Sensor Payload Buffer
__attribute__((section(".scratch_buffer"))) uint8_t scratch_buffer[SIZE_OF_SCRATCH_BUFFER];

// SPI Buffers
__attribute__((section(".spi_buffer_tx"))) uint8_t spi_buffer_tx[ADF_SPI_BUFFER_SIZE];
__attribute__((section(".spi_buffer_rx"))) uint8_t spi_buffer_rx[ADF_SPI_BUFFER_SIZE];

// GLobal State Machine Struct
gStateMachine_t globalSM = {.connection_status = false, .board_id = 0, .cmd_current = 0, .cmd_next = 0, .errors = 0, .test_running = false};

/* Prototype */
static void xintCallback(void* pCBParam, uint32_t nEvent, void* pEventData);

int main(int argc, char* argv[]) {
    uint32_t        eInitResult;
    ADI_PWR_RESULT  ePwrResult;
    ADI_UART_RESULT eUartResult;
    ADI_RNG_RESULT  eRNGResult;

    eInitResult = adi_initComponents();
    DEBUG_MESSAGE("Failed to intialize the power service\n", startup, eInitResult, 0);

    ePwrResult = adi_pwr_Init();
    DEBUG_MESSAGE("Failed to intialize the power service\n", startup, ePwrResult, ADI_PWR_SUCCESS);

    ePwrResult = adi_pwr_SetClockDivider(ADI_CLOCK_HCLK, 1);
    DEBUG_MESSAGE("Failed to intialize the power service\n", startup, ePwrResult, ADI_PWR_SUCCESS);

    ePwrResult = adi_pwr_SetClockDivider(ADI_CLOCK_PCLK, 1);
    DEBUG_MESSAGE("Failed to intialize the power service\n", startup, ePwrResult, ADI_PWR_SUCCESS);

    ePwrResult = adi_pwr_UpdateCoreClock();
    DEBUG_MESSAGE("Failed to update system clks\n", startup, ePwrResult, ADI_PWR_SUCCESS);

    eUartResult = adi_uart_Open(UART_DEVICE_NUM, ADI_UART_DIR_BIDIRECTION, UartDeviceMem, ADI_UART_MEMORY_SIZE, &uartDevice);
    DEBUG_MESSAGE("Failed to open the UART device.\n", startup, eUartResult, ADI_UART_SUCCESS);

    /* Register a callback. */
    eUartResult = adi_uart_RegisterCallback(uartDevice, UARTCallback, NULL);
    DEBUG_MESSAGE("Call back registration failed\n", startup, eUartResult, ADI_UART_SUCCESS);

    /* Initialize GPIO service with number of callbacks required */
    ADI_GPIO_RESULT eGpioResult;
    eGpioResult = adi_gpio_Init(GPIOCallbackMem, ADI_GPIO_MEMORY_SIZE);
    DEBUG_MESSAGE("adi_gpio Init\n", startup, eGpioResult, ADI_GPIO_SUCCESS);

    eRNGResult = adi_rng_Open(RNG_DEV_NUM, RngDevMem, sizeof(RngDevMem), &rngDevice);
    DEBUG_MESSAGE("Failed to open RNG device", rng, eRNGResult, ADI_RNG_SUCCESS);

    eRNGResult = adi_rng_SetSampleLen(rngDevice, RNG_DEV_LEN_PRESCALER, RNG_DEV_LEN_RELOAD);
    DEBUG_MESSAGE("Failed to set sample length", rng, eRNGResult, ADI_RNG_SUCCESS);

    // eRNGResult = adi_rng_RegisterCallback(rngDevice, rngCallback, rngDevice);
    // DEBUG_MESSAGE("Failed to register callback", rng, eRNGResult, ADI_RNG_SUCCESS);

    eRNGResult = adi_rng_Enable(rngDevice, true);
    DEBUG_MESSAGE("Failed to enable device", rng, eRNGResult, ADI_RNG_SUCCESS);

    /* LEDS */
    printf("[MAIN] Enable LEDS\n");
    leds_init();

    // Blink LED on startup
    for (uint8_t i = 0; i < 8; i++) {
        led_on(1);
        delay_ms(100);
        led_off(1);
        delay_ms(100);
    }

    /* Register the callback for XINT0 external interrupts  */
    adi_gpio_InputEnable(ADI_GPIO_PORT1, ADI_GPIO_PIN_0, true);
    ADI_XINT_RESULT eXintResult;
    eXintResult = adi_xint_Init(xintMemory, ADI_XINT_MEMORY_SIZE);
    DEBUG_MESSAGE("adi_xint_Init", startup, eXintResult, ADI_XINT_SUCCESS);
    eXintResult = adi_xint_RegisterCallback(ADI_XINT_EVENT_INT1, xintCallback, NULL);
    DEBUG_MESSAGE("adi_xint_RegisterCallback", startup, eXintResult, ADI_XINT_SUCCESS);
    /* Enable XINT0 for falling edge interrupt */
    eXintResult = adi_xint_EnableIRQ(ADI_XINT_EVENT_INT1, ADI_XINT_IRQ_RISING_EDGE);
    DEBUG_MESSAGE("adi_xint_EnableIRQ", startup, eXintResult, ADI_XINT_SUCCESS);

    /* Submit an empty buffer to the driver for receiving data using DMA mode. */
    eUartResult = adi_uart_SubmitRxBuffer(uartDevice, uart_rx_buffer, UART_CMD_HEADER_NUM_BYTES, true);
    DEBUG_MESSAGE("Failed to submit the Rx buffer 0 using DMA mode.", startup, eUartResult, ADI_UART_SUCCESS);

    /* SPI to Sensor */
    // ADI_SPI_RESULT eSPIResult;
    // eSPIResult = adf_spi_init(&spiDevice, spiDeviceMem);
    // DEBUG_MESSAGE("Failed init SPI", startup, eSPIResult, ADI_SPI_SUCCESS);
    led_off(0);
    uctest_setup_commands_map();
    // Main Loop
    while (true) {
        if (globalSM.cmd_next) { // If a valid command has been received
            led_on(0);
            process_command();
            led_off(0);
        }
        __WFI();
    }

    return 1;
}

static void xintCallback(void* pCBParam, uint32_t nEvent, void* pEventData) {
    if ((ADI_XINT_EVENT)nEvent == ADI_XINT_EVENT_INT1) {
        // Stop any active test
        globalSM.test_running = false;
    }
}

void HardFault_Handler(void) {

    while (1) {
        __NOP();
    }
}
