#include <drivers/gpio/adi_gpio.h>

#include "statemachine_gui.h"
#include "adf_timers.h"

__NO_RETURN void error_indicator(void) {

  while(1) {

    adi_gpio_SetHigh(ADI_GPIO_PORT1, ADI_GPIO_PIN_13);
    delay_ms(500);
    adi_gpio_SetLow(ADI_GPIO_PORT1, ADI_GPIO_PIN_13);
    delay_ms(500);

  }
}
