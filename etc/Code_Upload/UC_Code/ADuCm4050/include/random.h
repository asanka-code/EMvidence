#ifndef _RANDOM_H
#define _RANDOM_H

/* RNG Driver includes */
#include <drivers/rng/adi_rng.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Enable macro to build example in callback mode.
 * We allow the macro to be defined outside the header for ease of testing
 */
#if !defined(RNG_ENABLE_CALLBACK)
#define RNG_ENABLE_CALLBACK (0u)
#endif

/* Number of random numbers to read */
#define NUM_RANDOM_NUMS (5u)

/* RNG Device number */
#define RNG_DEV_NUM (0u)

/* Sample Len Prescaler value to be set. This value is only required if the
 * value needs to be changed dynamically. Otherwise, RNG0_CFG_LENGTH_RELOAD
 * in adi_rng_config.h can be used.
 */
#define RNG_DEV_LEN_PRESCALER (1u)

/* Sample Len Reload value to be set. This value is only required if the
 * value needs to be changed dynamically. Otherwise, RNG0_CFG_LENGTH_RELOAD
 * in adi_rng_config.h can be used. */
#define RNG_DEV_LEN_RELOAD (256u)

void rngCallback(void* pCBParam, uint32_t Event, void* pArg);
void random_gen(uint8_t* buffer, uint32_t num_random_bytes);
void test_rng(uint32_t lrn_buffer);

#endif // _RANDOM_H
