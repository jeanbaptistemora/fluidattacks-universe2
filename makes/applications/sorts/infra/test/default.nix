{ terraformTest
, ...
}:
terraformTest {
  name = "sorts-infra-test";
  product = "sorts";
  target = "sorts/infra";
}
