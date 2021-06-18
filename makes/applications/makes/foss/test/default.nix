{ terraformTest
, ...
}:
terraformTest {
  name = "makes-foss-test";
  product = "makes";
  target = "makes/applications/makes/foss/src";
}
