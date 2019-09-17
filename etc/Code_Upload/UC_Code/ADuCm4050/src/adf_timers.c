#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

#include <drivers/tmr/adi_tmr.h>
#include <drivers/pwr/adi_pwr.h>
#include "adf_timers.h"

volatile bool bTimeOutFlag0;
volatile bool bTimeOutFlag1;

/**
 * @brief  Callback for GPT-1. Does nothing for this example
 */
/*
static void GPTimer1Callback(void *pCBParam, uint32_t Event, void *pArg) {
    switch (Event) {
    case ADI_TMR_EVENT_TIMEOUT:
        break;
    case ADI_TMR_EVENT_CAPTURE:
        break;
    default:
        break;
    }
}
*/

/**
 * @brief  Callback for GPT-0. Set the boolean flag to corresponding to the the event occured.
 */
void GPTimer0Callback(void *pCBParam, uint32_t Event, void *pArg) {
    switch (Event) {
    case ADI_TMR_EVENT_TIMEOUT:
        bTimeOutFlag0 = true;
        break;
    case ADI_TMR_EVENT_CAPTURE:
        break;
    default:
        break;
    }
}

/**
 * @brief  Callback for GPT-0. Set the boolean flag to corresponding to the the event occured.
 */
void GPTimer1Callback(void *pCBParam, uint32_t Event, void *pArg) {
    switch (Event) {
    case ADI_TMR_EVENT_TIMEOUT:
        bTimeOutFlag1 = true;
        break;
    case ADI_TMR_EVENT_CAPTURE:
        break;
    default:
        break;
  }
}

void timer_start_s(ADI_TMR_DEVICE nDeviceNum, uint32_t nTimerCount) { // 1ms

    ADI_TMR_CONFIG tmrConfig;

    if (nDeviceNum==ADI_TMR_DEVICE_GP0) {
        adi_tmr_Init(nDeviceNum, GPTimer0Callback, NULL, true);
    } else if (nDeviceNum==ADI_TMR_DEVICE_GP1) {
        adi_tmr_Init(nDeviceNum, GPTimer1Callback, NULL, true);
    }
    
    /* Configure GP0 to have a period of 10 ms */
    tmrConfig.bCountingUp  = false;
    tmrConfig.bPeriodic    = true;
    tmrConfig.ePrescaler   = ADI_TMR_PRESCALER_256;
    tmrConfig.eClockSource = ADI_TMR_CLOCK_LFOSC;
    tmrConfig.nLoad        = GP0_LOAD_VALUE_FOR_1S_PERIOD * nTimerCount;
    tmrConfig.nAsyncLoad   = GP0_LOAD_VALUE_FOR_1S_PERIOD * nTimerCount;
    tmrConfig.bReloading   = false;
    tmrConfig.bSyncBypass  = false;

    adi_tmr_ConfigTimer(nDeviceNum, &tmrConfig);

    if (nDeviceNum==ADI_TMR_DEVICE_GP0) {
        bTimeOutFlag0= false;
    } else if (nDeviceNum==ADI_TMR_DEVICE_GP1) {
        bTimeOutFlag1= false;
    }

    adi_tmr_Enable(nDeviceNum, true);
}


void timer_start_ms(ADI_TMR_DEVICE nDeviceNum, uint32_t nTimerCount) { // 1ms

    ADI_TMR_CONFIG tmrConfig;

    if (nDeviceNum==ADI_TMR_DEVICE_GP0) {
        adi_tmr_Init(nDeviceNum, GPTimer0Callback, NULL, true);
    } else if (nDeviceNum==ADI_TMR_DEVICE_GP1) {
        adi_tmr_Init(nDeviceNum, GPTimer1Callback, NULL, true);
    }
    
    /* Configure GP0 to have a period of 10 ms */
    tmrConfig.bCountingUp  = false;
    tmrConfig.bPeriodic    = true;
    tmrConfig.ePrescaler   = ADI_TMR_PRESCALER_64;
    tmrConfig.eClockSource = ADI_TMR_CLOCK_HFOSC;
    tmrConfig.nLoad        = GP0_LOAD_VALUE_FOR_1MS_PERIOD * nTimerCount;
    tmrConfig.nAsyncLoad   = GP0_LOAD_VALUE_FOR_1MS_PERIOD * nTimerCount;
    tmrConfig.bReloading   = false;
    tmrConfig.bSyncBypass  = false;
    adi_tmr_ConfigTimer(ADI_TMR_DEVICE_GP0, &tmrConfig);
    
    if (nDeviceNum==ADI_TMR_DEVICE_GP0) {
        bTimeOutFlag0= false;
    } else if (nDeviceNum==ADI_TMR_DEVICE_GP1) {
        bTimeOutFlag1= false;
    }

    adi_tmr_Enable(nDeviceNum, true);
}

void timer_start(ADI_TMR_DEVICE nDeviceNum, uint32_t nTimerCount) { // 100us

    ADI_TMR_CONFIG tmrConfig;

    if (nDeviceNum==ADI_TMR_DEVICE_GP0) {
        adi_tmr_Init(nDeviceNum, GPTimer0Callback, NULL, true);
    } else if (nDeviceNum==ADI_TMR_DEVICE_GP1) {
        adi_tmr_Init(nDeviceNum, GPTimer1Callback, NULL, true);
    }

    /* Configure GP0 to have a period of 10 ms */
    tmrConfig.bCountingUp  = false;
    tmrConfig.bPeriodic    = true;
    tmrConfig.ePrescaler   = ADI_TMR_PRESCALER_1;
    tmrConfig.eClockSource = ADI_TMR_CLOCK_HFOSC;
    tmrConfig.nLoad        = GP0_LOAD_VALUE_FOR_100US_PERIOD * nTimerCount;
    tmrConfig.nAsyncLoad   = GP0_LOAD_VALUE_FOR_100US_PERIOD * nTimerCount;
    tmrConfig.bReloading   = false;
    tmrConfig.bSyncBypass  = false;
    adi_tmr_ConfigTimer(ADI_TMR_DEVICE_GP0, &tmrConfig);

    if (nDeviceNum==ADI_TMR_DEVICE_GP0) {
        bTimeOutFlag0= false;
    } else if (nDeviceNum==ADI_TMR_DEVICE_GP1) {
        bTimeOutFlag1= false;
    }

    adi_tmr_Enable(nDeviceNum, true);
    
}

void timer_stop(ADI_TMR_DEVICE nDeviceNum) {
    adi_tmr_Enable(nDeviceNum, false);
    adi_tmr_Init(nDeviceNum, NULL, NULL, false);
}


/**
 * @brief Delay for a set time in milliseconds
 * @param[in] u32Duration Delay duration in milliseconds
 */
void delay_ms(uint32_t u32Duration) {
    for (uint32_t i = 0; i < u32Duration; i++)
        delay_us(1000);
}

/**
 * @brief Delay for a set time  in microseconds.
 * @param[in] u32Duration Delay duration in microseconds
 */
void delay_us(uint32_t u32Duration) {
    uint64_t duration = (u32Duration * 10569) >> 12;
    for (uint32_t i = 0; i < duration; i++) {
        __NOP();
    }
}
