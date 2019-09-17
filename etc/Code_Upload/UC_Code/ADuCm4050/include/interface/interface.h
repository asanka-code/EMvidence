#ifndef _GUI_INTERFACE_H_
#define _GUI_INTERFACE_H_

#include "config.h"
#include <stdbool.h>

#define CALIBRATION_RESULTS_LEN 15
#define SIZE_OF_SCRATCH_BUFFER 4096

typedef enum {
    // ADuCM302x commands (0x100 to 0x1FF)
    cmd_get_fw_info       = 0x101,
    cmd_flash_LEDs        = 0x102,
    cmd_set_LEDs          = 0x103,
    cmd_mcu_gpio_enable   = 0x104,
    cmd_mcu_gpio_set      = 0x105,
    cmd_mcu_gpio_get      = 0x106,
    cmd_loop_back         = 0x109,
    cmd_get_driver_device = 0x10A,
    cmd_set_driver_device = 0x10B,
    cmd_clear_errors      = 0x10C,

    // State Machine Functions
    cmd_sm_set_board_id = 0x501,
    cmd_sm_get_board_id = 0x502,

    // Unit tests for functionality
    cmd_utest_timeout = 0x901,

} adf_command_t;

// Prototypes
void process_command(void);
bool check_command(void);

#endif // _GUI_INTERFACE_H_
