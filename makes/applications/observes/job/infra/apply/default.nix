{ observesPkgsTerraform
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path observesPkgsTerraform;
in
terraformApply {
  name = "observes-job-infra-apply";
  product = "observes";
  target = "observes/infra/terraform";
}
