{ terraformApply
, ...
}:
terraformApply {
  name = "sorts-infra-deploy";
  product = "sorts";
  target = "sorts/infra";
}
