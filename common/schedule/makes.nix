# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonSchedule = {
        setup = [outputs."/secretsForAwsFromEnv/prodCommon"];
        src = "/common/schedule/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonSchedule = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/common/schedule/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      commonSchedule = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/common/schedule/infra";
        version = "1.0";
      };
    };
  };
}
