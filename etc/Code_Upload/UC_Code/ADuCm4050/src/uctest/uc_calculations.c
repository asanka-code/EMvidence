#include <stdint.h>

// Generated in Python: ", ".join([str(round(random.random() * 255)) for i in range(255)])
#define ARRAY_1_LEN 8
uint32_t array_1[ARRAY_1_LEN] = {45, 161, 183, 89, 23, 205, 120, 7};

// Generated: ", ".join([f"{random.random() * 255:.2f}" for i in range(127)])
#define ARRAY_2_LEN 8
float array_2_float[ARRAY_2_LEN] = {14.47, 89.36, 135.68, 12.08, 64.36, 136.54, 246.82, 200.54};

void calc_additions(void) {
    for (uint8_t i = 0; i < ARRAY_1_LEN; i++) {
        array_1[i] = array_1[i] + array_1[i];
    }
}
void calc_subtractions(void) {
    for (uint8_t i = 0; i < ARRAY_1_LEN; i++) {
        array_1[i] = array_1[i] - array_1[i];
    }
}

void calc_float_mult(void) {
    for (uint8_t i = 0; i < ARRAY_1_LEN; i++) {
        array_2_float[i] = array_2_float[i] * 2.1;
    }
}
