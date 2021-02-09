{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgsTerraform;
in
terraformApply {
  name = "serves-users-forces-apply";
  product = "serves";
  target = "serves/users/forces/terraform";
}
