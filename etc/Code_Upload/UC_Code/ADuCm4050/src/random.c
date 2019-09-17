/* RNG example include */
#include "random.h"
#include "include/common_debug.h"
#include "include/statemachine_gui.h"
/* Managed drivers and/or services include */
#include <drivers/pwr/adi_pwr.h>
#include <drivers/rng/adi_rng.h>
/*=============  D A T A  =============*/

/* RNG Device Handle */
extern ADI_RNG_HANDLE rngDevice;
/* Data buffers for Random numbers */
static uint32_t RNBuff[NUM_RANDOM_NUMS] = {0};

static volatile uint32_t nNumRNGen = 0u;

static volatile bool failure_detected = false;

static volatile bool stuck_status_detected = false;

extern gStateMachine_t globalSM;

/*
 *  Callback from RNG Driver
 *
 * Parameters
 *  - [in]  pCBParam    Callback parameter supplied by application
 *  - [in]  Event       Callback event
 *  - [in]  pArg        Callback argument
 *
 * Returns  None
 *
 */
void rngCallback(void* pCBParam, uint32_t Event, void* pArg) {
    ADI_RNG_RESULT eRNGResult = ADI_RNG_SUCCESS;
    uint32_t       nRandomNum = 0;
    if (Event == ADI_RNG_EVENT_READY) {
        eRNGResult = adi_rng_GetRngData(rngDevice, &nRandomNum);
        if (ADI_RNG_SUCCESS != eRNGResult) {
            /* A failure has been detected. Since we cannot print this from the ISR
             * we set a variable to indicate the problem.
             */
            failure_detected = true;
            return;
        }
        /* Make sure that we do not overflow the array allocated */
        if (nNumRNGen < NUM_RANDOM_NUMS) {
            RNBuff[nNumRNGen++] = nRandomNum;
        }
    } else if (Event == ADI_RNG_EVENT_STUCK) {
        stuck_status_detected = true;
    } else {
        /* Unknown event */
        failure_detected = true;
    }
}

void random_gen(uint8_t* buffer, uint32_t num_random_bytes) {
    ADI_RNG_RESULT eRNGResult;
    bool           bRNGRdy = false;
    uint32_t       nRNGgen = 0;
    while (nRNGgen < num_random_bytes) {
        eRNGResult = adi_rng_GetRdyStatus(rngDevice, &bRNGRdy);
        DEBUG_MESSAGE("Failed to get ready status", rng, eRNGResult, ADI_RNG_SUCCESS);
        if (bRNGRdy) {
            uint32_t nRandomNum;
            eRNGResult = adi_rng_GetRngData(rngDevice, &nRandomNum);
            DEBUG_MESSAGE("Failed to enable device", rng, eRNGResult, ADI_RNG_SUCCESS);

            buffer[nRNGgen++] = nRandomNum & 0xFF;
        }
    }
}

static uint8_t temp_buffer[32] = {0};

void test_rng(uint32_t lrn_buffer) {
    if (lrn_buffer < 32) {

        random_gen(temp_buffer, lrn_buffer);
        for (uint8_t ir = 0; ir < lrn_buffer; ir++) {
            printf("%d ", temp_buffer[ir]);
        }
    }
}