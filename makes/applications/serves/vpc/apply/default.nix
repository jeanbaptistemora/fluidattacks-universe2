{ servesPkgs
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-vpc-apply";
  product = "serves";
  target = "serves/vpc/terraform";
  secretsPath = "serves/secrets/production.yaml";
}
