#! __envShell__
# shellcheck shell=bash

# Setup the path
export PATH="__envRuntimeBinPath__:${PATH:-}"

# Setup linked path
export LD_LIBRARY_PATH="__envRuntimeLibPath__:${LD_LIBRARY_PATH:-}";

# Setup the python path
export PYTHONPATH="__envPythonRequirements__:${PYTHONPATH:-}"
export PYTHONPATH="__envSrcSkimsSkims__:${PYTHONPATH:-}"

# Context artifacts
export SKIMS_CIPHER_SUITES_PATH='__envSrcSkimsStatic__/cryptography/cipher_suites.csv'
export SKIMS_FLUID_WATERMARK='__envSrcSkimsStatic__/img/logo_fluid_attacks_854x329.png'
export SKIMS_PARSER_ANTLR='__envParserAntlr__/build/install/parse/bin/parse'
export SKIMS_PARSER_BABEL='__envParserBabel__'
export SKIMS_ROBOTO_FONT='__envSrcSkimsVendor__/fonts/roboto_mono_from_google/regular.ttf'
export SKIMS_STATIC='__envSrcSkimsStatic__'
export SKIMS_VENDOR='__envSrcSkimsVendor__'

# Invoke the entrypoint
'__envPython__' '__envSrcSkimsSkims__/cli/__init__.py' "${@}"
