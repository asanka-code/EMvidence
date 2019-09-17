#include "include/leds.h"
#include <drivers/gpio/adi_gpio.h>

void leds_init(void) {
    adi_gpio_OutputEnable(LED0_PORT, LED0_PIN, true);
    adi_gpio_OutputEnable(LED1_PORT, LED1_PIN, true);
}

void led_on(uint8_t led) {
    if (led == 0) {
        adi_gpio_SetLow(LED0_PORT, LED0_PIN);
    } else if (led == 1) {
        adi_gpio_SetLow(LED1_PORT, LED1_PIN);
    }
}
void led_off(uint8_t led) {
    if (led == 0) {
        adi_gpio_SetHigh(LED0_PORT, LED0_PIN);
    } else if (led == 1) {
        adi_gpio_SetHigh(LED1_PORT, LED1_PIN);
    }
}
