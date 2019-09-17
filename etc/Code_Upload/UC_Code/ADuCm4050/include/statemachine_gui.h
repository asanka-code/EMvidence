#ifndef _STATEMACHINE_GUI_H_
#define _STATEMACHINE_GUI_H_

#include <stdbool.h>
#include <stdint.h>

/** @addtogroup STATEMACHINE
 * @{
 */

__attribute__((noreturn)) void error_indicator(void);

/**
 * @brief Global State Machine
 */
typedef struct {
    bool     connection_status; /**<  Heartbeat to check PC connectivity \todo */
    uint32_t board_id;          /**<  Board identifier, supplied by PC */
    uint32_t cmd_current;       /**<  Command being executed at the moment */
    uint32_t cmd_next;          /**<  Next command to be processed */
    bool     test_running;      /**<  Indicate if a test loop is runninf */
    union {
        uint8_t errors; /**< Contains Driver error and last Status */
        struct {
            uint8_t checksum : 1;      /**< Command CRC Failure  */
            uint8_t startup : 1;       /**< Failure to run startup routine  */
            uint8_t timeout : 1;       /**<  Timeout error */
            uint8_t cmd_not_found : 1; /**<  CMD not found anywhere error */
            uint8_t rng : 1;           /**<  RNG failure */
        } errors_b;
    };
} gStateMachine_t;

/** @} */ /* End of group STATEMACHINE */

#endif // _STATEMACHINE_GUI_H_
