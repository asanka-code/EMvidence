#ifndef __TIMERS_HEADER__
#define __TIMERS_HEADER__

#include <drivers/tmr/adi_tmr.h>

#define GP0_LOAD_VALUE_FOR_100US_PERIOD (631u)
#define GP0_LOAD_VALUE_FOR_1MS_PERIOD (406u)
#define GP0_LOAD_VALUE_FOR_1S_PERIOD (126u)

void timer_start(ADI_TMR_DEVICE nDeviceNum, uint32_t nCountMS);
void timer_start_ms(ADI_TMR_DEVICE nDeviceNum, uint32_t nCountMS);
void timer_start_s(ADI_TMR_DEVICE nDeviceNum, uint32_t nCountMS);
void timer_stop(ADI_TMR_DEVICE nDeviceNum);
void GPTimer0Callback(void *pCBParam, uint32_t Event, void *pArg);
// void GPTimer1Callback(void *pCBParam, uint32_t Event, void *pArg);
void delay_ms(uint32_t u32Duration);
void delay_us(uint32_t u32Duration);

#endif
