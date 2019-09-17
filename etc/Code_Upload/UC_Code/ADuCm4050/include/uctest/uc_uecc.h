#ifndef __UC_UECC_H_
#define __UC_UECC_H_

#include <stdint.h>

#define HASH_LEN 32

void uecc_make_key();
void uecc_sign();
void uecc_verify();
void uecc_random_hash();
void uecc_select_curve();

#endif
