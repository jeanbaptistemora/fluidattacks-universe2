# shellcheck shell=bash

function asserts {
  python3.7 -c 'from fluidasserts.utils.cli import main; main()' -- "${@}"
}
