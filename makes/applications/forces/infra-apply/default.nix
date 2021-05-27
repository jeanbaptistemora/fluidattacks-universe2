{ terraformApply
, ...
}:
terraformApply {
  name = "terraform-apply";
  product = "forces";
  target = "forces/infra";
}
