project(
  'testUC',
  'c',
  version: '0.0.1',
  license: [
    'MIT',
  ],
  default_options: [
    'c_std=c11',
  ],
)


# Options
platform = get_option('platform')
build = get_option('buildtype')
pack_root = get_option('pack_root')


# Configuration
conf_data = configuration_data()
conf_data.set('BUILD_DAY', 27)
if build == 'debug'
  conf_data.set('BUILD_DEBUG', 1)
elif build == 'release'
  conf_data.set('BUILD_RELEASE', 1)
endif
conf_data.set('BUILD_MONTH', 11)
conf_data.set('BUILD_YEAR', 17)
conf_data.set('BUILD_VERSION', 1)
conf_data.set(platform, 1)
configure_file(output : 'config.h',
               configuration : conf_data)
configuration_include = ['.']

# Platform Support (ADuCM3049 or ADuCM4050)
subdir('RTE')


uecc_sources = [
  'src/uecc/uECC.c'
]

# Sources for UCTest files
uctest_source = [
  'src/uctest/uc_calculations.c',
  'src/uctest/uc_loops.c',
  'src/uctest/uc_uecc.c',
]

# Main Definitions
main_sources = [
  'src/main.c',
  'src/adf_spi.c',
  'src/adf_timers.c',
  'src/adf_uart.c',
  'src/leds.c',
  'src/random.c',
  'src/crc.c',
  'src/map.c',
  'src/interface.c',
  'src/interface_uctest.c',
  'src/statemachine.c',
  'src/uart_buffer.c',
  support_sources,
  uecc_sources,
  uctest_source
]

main_includes = include_directories([
  'include',
  'include/interface',
  'include/uctest',
  'system',
  support_includes,
  configuration_include
])


if micro == '3029'
  main = executable(
      'main',
      sources: main_sources,
      include_directories: main_includes,
      install: true,
  )
  
elif micro == '4050'

  main = executable(
      'main',
      sources: main_sources,
      include_directories: main_includes,
      link_with: math_lib,
      install: true,
  )

endif
