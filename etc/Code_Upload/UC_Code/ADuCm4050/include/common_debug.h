
#ifndef __post_common_h__
#define __post_common_h__

#include <adi_processor.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if BUILD_DEBUG
#define DEBUG_MESSAGE(msg, error_bit, result, expected_value)                                                                              \
    do {                                                                                                                                   \
        if ((result) != (expected_value)) {                                                                                                \
            printf("[ERROR]\n");                                                                                                           \
            printf(msg);                                                                                                                   \
            globalSM.errors_b.error_bit = 1;                                                                                               \
            while (1) {                                                                                                                    \
                __WFI();                                                                                                                   \
            }                                                                                                                              \
        }                                                                                                                                  \
    } while (0)

#else

#define DEBUG_MESSAGE(msg, error_bit, result, expected_value)                                                                              \
    do {                                                                                                                                   \
        if ((result) != (expected_value)) {                                                                                                \
            globalSM.errors_b.error_bit = 1;                                                                                               \
            while (1) {                                                                                                                    \
                __WFI();                                                                                                                   \
            }                                                                                                                              \
        }                                                                                                                                  \
    } while (0)

#endif

#endif /* __POST_COMMON_H__ */
