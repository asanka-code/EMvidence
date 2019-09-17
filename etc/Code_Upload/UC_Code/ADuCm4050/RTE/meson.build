if platform == 'EZ_KIT'
  micro = '3029'
elif platform == 'COG3029' 
  micro = '3029'
elif platform == 'COG4050' 
  micro = '4050'
elif platform == 'DUAL_BOARD' 
  micro = '4050'
endif

# Compile flags
if micro == '3029'
  mcu_cflags = [
    '-mcpu=cortex-m3', '-mthumb', '-lm',
    '-DCORE0', '-D_RTE_', '-D__ADUCM3029__', '-D__SILICON_REVISION__=0xffff',
  ]
elif micro == '4050'
  mcu_cflags = [
    '-mcpu=cortex-m4', '-mthumb', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16',# '-DADI_DEBUG=1',
    '-DCORE0', '-D_RTE_', '-D__ADUCM4050__', '-D__SILICON_REVISION__=0xffff',
  ]
else
  error('Unsupported Board')
endif

debug_cflags = [
  '-g', '-gdwarf-2', '-ffunction-sections', '-fdata-sections', '-D_DEBUG'
]

release_cflags = [
  '-O1',  '-ffunction-sections' , '-fdata-sections', '-Wall', '-Wpedantic'
]

plaform_cflag = ['-D' + platform]

semihosting_cflags = [
  '--specs=rdimon.specs',
]

if build == 'debug'

  am_cflags = [
      mcu_cflags,
      plaform_cflag,
      debug_cflags,
      semihosting_cflags
  ]

elif build == 'release'

  am_cflags = [
      mcu_cflags,
      plaform_cflag,
      release_cflags
  ]

endif

add_global_arguments(am_cflags, language: 'c')

# Linker Args
if micro == '3029'
  rte_mapfile = 'Device/ADuCM3029/ADuCM3029.ld'
  mcu_lflags = ['-mcpu=cortex-m3', '-mthumb', '-lm']
elif micro == '4050'
  rte_mapfile = 'Device/ADuCM4050/ADuCM4050.ld'
  mcu_lflags = ['-mcpu=cortex-m4', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16', '-mthumb', '-lm']
endif

link_args_map = ['-Xlinker', '-Map=output.map']
semihosting_lflags = ['--specs=rdimon.specs', '-lc', '-lrdimon']

if build == 'debug'

  link_args = [
    mcu_lflags,
    ['-Wl,--gc-sections'],
    link_args_map,
    semihosting_lflags,
    '-T@0@/@1@'.format(meson.current_source_dir(), rte_mapfile)
  ]

elif build == 'release'

  link_args = [
    mcu_lflags,
    '-Wl,--gc-section',
    link_args_map,
    '-T@0@/@1@'.format(meson.current_source_dir(), rte_mapfile)
  ]

endif

add_project_link_arguments(link_args, language: 'c')

# ADuCM3029 Support
if micro == '3029'
  rte_sources = [
    'RTE/Device/ADuCM3029/startup_ADuCM3029.c',
    'RTE/Device/ADuCM3029/system_ADuCM3029.c'
  ]

  rte_includes = [
    'RTE/Device/ADuCM3029'
  ]

  dfp_sources = [
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/gpio/adi_gpio.c',
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/spi/adi_spi.c',
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/uart/adi_uart.c',
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/dma/adi_dma.c',
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/pwr/adi_pwr.c',
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/i2c/adi_i2c.c',
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/xint/adi_xint.c',
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/tmr/adi_tmr.c',
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Source/drivers/rng/adi_rng.c'
  ]

  dfp_includes = [
    pack_root + 'AnalogDevices/ADuCM302x_DFP/2.0.0/Include'
  ]

elif micro == '4050'
 
  rte_sources = [
    'RTE/Device/ADuCM4050/startup_ADuCM4050.c',
    'RTE/Device/ADuCM4050/system_ADuCM4050.c',
    'RTE/Device/ADuCM4050/reset_ADuCM4050.S'
  ]

  rte_includes = [
    'RTE/Device/ADuCM4050'
  ]

  dfp_sources = [
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/gpio/adi_gpio.c',
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/spi/adi_spi.c',
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/uart/adi_uart.c',
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/dma/adi_dma.c',
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/pwr/adi_pwr.c',
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/i2c/adi_i2c.c',
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/xint/adi_xint.c',
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/tmr/adi_tmr.c',
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Source/drivers/rng/adi_rng.c'
  ]

  dfp_includes = [
    pack_root + 'AnalogDevices/ADuCM4x50_DFP/3.2.0/Include'
  ]

  math_lib = static_library(pack_root + 'ARM/CMSIS/5.4.0/CMSIS/Lib/GCC/libarm_cortexM4lf_math.a')

endif

generated_sources = [
  'system/adi_initialize.c',
  'src/pinmux_config.c'
]

cmsis_includes = [
  pack_root + 'ARM/CMSIS/5.4.0/CMSIS/Include',   
]

support_sources = [
    rte_sources,
    generated_sources,
    dfp_sources
]

support_includes = [
    rte_includes,
    dfp_includes,
    cmsis_includes
]
