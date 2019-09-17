#!/bin/bash
meson --buildtype=debug --cross-file cross_file.txt -Dplatform=COG4050 -Dbuild=DEBUG DebugCOG4050 -Dpack_root=/opt/packs/
