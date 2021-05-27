{ terraformApply
, ...
}:
terraformApply {
  name = "forces-infra-deploy";
  product = "forces";
  target = "forces/infra";
}
