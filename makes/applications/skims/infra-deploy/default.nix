{ terraformApply
, ...
}:
terraformApply {
  name = "skims-infra-deploy";
  product = "skims";
  target = "skims/infra";
}
