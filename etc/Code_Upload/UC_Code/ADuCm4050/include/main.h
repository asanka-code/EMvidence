#ifndef _MAIN_H_
#define _MAIN_H_

#include <drivers/gpio/adi_gpio.h>
#include <drivers/pwr/adi_pwr.h>

// Function Prototypes
ADI_PWR_RESULT  bsp_init(void);
ADI_GPIO_RESULT pin_init(void);

/* Memory required by the driver for bidirectional mode of operation. */
#define ADI_UART_MEMORY_SIZE (ADI_UART_BIDIR_MEMORY_SIZE)

/* Size of the data buffers that will be processed. */
#define SIZE_OF_BUFFER 26u
/* Timeout value for receiving data. */
#define UART_GET_BUFFER_TIMEOUT 1000000u

#endif // _MAIN_H_
