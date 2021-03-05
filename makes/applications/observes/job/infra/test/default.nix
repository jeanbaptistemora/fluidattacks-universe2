{ terraformTest
, ...
}:
terraformTest {
  name = "observes-job-infra-test";
  product = "observes";
  target = "observes/infra/terraform";
}
