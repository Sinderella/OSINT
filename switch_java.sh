#!/bin/sh
set -ex
wget https://github.com/michaelklishin/jdk_switcher/raw/master/jdk_switcher.sh
chmod +x jdk_switcher.sh
./jdk_switcher.sh use oraclejdk8
./jdk_switcher.sh home oraclejdk8
