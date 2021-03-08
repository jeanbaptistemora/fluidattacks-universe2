{ terraformApply
, ...
}:
terraformApply {
  name = "integrates-infra-front-apply";
  product = "integrates";
  target = "integrates/deploy/front/terraform";
}
