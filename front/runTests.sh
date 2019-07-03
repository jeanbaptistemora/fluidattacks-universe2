#!/bin/bash
set -e
set -o pipefail

jest --detectOpenHandles
mv coverage/lcov.info coverage.lcov
rm -r coverage
