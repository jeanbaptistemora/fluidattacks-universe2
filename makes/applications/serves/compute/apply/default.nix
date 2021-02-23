{ servesPkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-compute-apply";
  product = "serves";
  target = "serves/compute/terraform";
}
