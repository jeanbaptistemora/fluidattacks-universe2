{ terraformTest
, ...
}:
terraformTest {
  name = "forces-infra-test";
  product = "forces";
  target = "forces/infra";
}
