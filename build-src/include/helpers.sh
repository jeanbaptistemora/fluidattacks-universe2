# shellcheck shell=bash

function camel_case_to_title_case {
  # Turn 'something_like_this' to 'SomethingLikeThis'
  IFS=_ read -ra str <<<"${1}"
  printf '%s' "${str[@]^}"
}
