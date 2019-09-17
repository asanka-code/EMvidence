#ifndef _CRC_H_
#define _CRC_H_
#include <stdint.h>

uint16_t crc16(const uint8_t* pbuffer, uint8_t buffer_length, uint16_t seed);

#endif // _CRC_H_
