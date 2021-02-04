{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgsTerraform;
in
terraformApply {
  name = "serves-user-forces-apply";
  product = "serves";
  target = "serves/services/user-provision/forces/terraform";
}
