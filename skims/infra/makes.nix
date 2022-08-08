# https://github.com/fluidattacks/makes
{
  deployTerraform = {
    modules = {
      skims = {
        src = "/skims/infra/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      skims = {
        src = "/skims/infra/src";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      skims = {
        src = "/skims/infra/src";
        version = "1.0";
      };
    };
  };
}
