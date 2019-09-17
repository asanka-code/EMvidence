#ifndef _LEDS_H_
#define _LEDS_H_

#include <drivers/gpio/adi_gpio.h>

#define LED0_PORT ADI_GPIO_PORT2
#define LED0_PIN ADI_GPIO_PIN_2

#define LED1_PORT ADI_GPIO_PORT2
#define LED1_PIN ADI_GPIO_PIN_10

void leds_init(void);
void led_on(uint8_t led);
void led_off(uint8_t led);

#endif // _LEDS_H_
