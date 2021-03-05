{ terraformApply
, ...
}:
terraformApply {
  name = "observes-job-infra-apply";
  product = "observes";
  target = "observes/infra/terraform";
}
