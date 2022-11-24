# shellcheck shell=bash

case 'SunOS':
    if (-e /net/hermes/scrb) then
#                  NRLSSC
      setenv S     /net/hermes/scrb/${user}/$P
      setenv W     /net/hermes/scrb/metzger/force/$N
    else
#                  NAVO MSRC
      mkdir        /scr/${user}
      chmod 754   /scr/${user}
      chmod 750   /scr/${user}
      setenv S     /scr/${user}/$P
      setenv W     /u/home/metzger/force/$N
    endif
    breaksw
