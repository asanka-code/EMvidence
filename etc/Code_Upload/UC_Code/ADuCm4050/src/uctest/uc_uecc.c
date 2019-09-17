#include "include/uctest/uc_uecc.h"
#include "include/adf_uart.h"
#include "include/random.h"
#include "include/uart_buffer.h"
#include "include/uecc/uECC.h"
#include <stddef.h>
#include <stdint.h>
#include <string.h>
extern uint8_t uart_rx_buffer[SIZE_OF_RX_BUFFER];

typedef struct {
    uint8_t private[32];    /**< Private Key  */
    uint8_t public[64];     /**< Public Key  */
    uint8_t hash[HASH_LEN]; /**< Hash  */
    uint8_t sig[64];        /**< Signature  */
    uint8_t curve_choice;   /**< Picks the selected curve from an array  */

    const struct uECC_Curve_t* curve; /**< Selected Curve  */
} gUECC_t;

gUECC_t globalUECC = {
    .private      = {0},
    .public       = {0},
    .hash         = {0},
    .sig          = {0},
    .curve        = NULL,
    .curve_choice = 0,
};

void uecc_make_key() {
    // Set up lobal Variables

    // Init everything to zero.
    memset(globalUECC.private, 0, sizeof globalUECC.private);
    memset(globalUECC.public, 0, sizeof globalUECC.public);
    memset(globalUECC.hash, 0, sizeof globalUECC.hash);
    memset(globalUECC.sig, 0, sizeof globalUECC.sig);
    globalUECC.curve = NULL;

    const struct uECC_Curve_t* curves[5];
    curves[0] = uECC_secp160r1();
    curves[1] = uECC_secp192r1();
    curves[2] = uECC_secp224r1();
    curves[3] = uECC_secp256r1();
    curves[4] = uECC_secp256k1();

    globalUECC.curve = curves[globalUECC.curve_choice];
    uECC_make_key(globalUECC.public, globalUECC.private, globalUECC.curve);
}
void uecc_sign() { uECC_sign(globalUECC.private, globalUECC.hash, sizeof(globalUECC.hash), globalUECC.sig, globalUECC.curve); }
void uecc_verify() { uECC_verify(globalUECC.public, globalUECC.hash, sizeof(globalUECC.hash), globalUECC.sig, globalUECC.curve); }
void uecc_random_hash() { random_gen(globalUECC.hash, HASH_LEN); }
void uecc_select_curve() {
    const uint8_t curve     = uart_rx_buffer[0];
    globalUECC.curve_choice = curve;
}