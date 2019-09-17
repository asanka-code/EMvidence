/*
** adi_initialize.c source file generated on November 28, 2017 at 15:57:01.
**
** Copyright (C) 2000-2017 Analog Devices Inc., All Rights Reserved.
**
** This file is generated automatically. You should not modify this source file,
** as your changes will be lost if this source file is re-generated.
*/

#include <sys/platform.h>

#include "adi_initialize.h"

extern int32_t adi_initpinmux(void);

int32_t adi_initComponents(void)
{
    return adi_initpinmux(); /* auto-generated code (order:0) */
}


