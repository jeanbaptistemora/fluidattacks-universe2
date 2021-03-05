{ terraformTest
, ...
}:
terraformTest {
  name = "skims-infra-test";
  product = "skims";
  target = "skims/infra";
}
