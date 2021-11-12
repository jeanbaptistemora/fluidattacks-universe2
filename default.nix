let
  m = import (import ./makes.lock.nix).makesSrc;
in
{ inherit m; }
