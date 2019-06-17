#!/bin/bash
set -e
set -o pipefail

jest
mv coverage/lcov.info coverage.lcov
rm -r coverage
