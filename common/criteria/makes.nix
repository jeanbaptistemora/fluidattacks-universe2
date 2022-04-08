# https://github.com/fluidattacks/makes
{
  lintWithAjv = {
    "common/criteria/compliance" = {
      schema = "/common/criteria/src/compliance/schema.json";
      targets = ["/common/criteria/src/compliance/data.yaml"];
    };
    "common/criteria/requirements" = {
      schema = "/common/criteria/src/requirements/schema.json";
      targets = ["/common/criteria/src/requirements/data.yaml"];
    };
    "common/criteria/vulnerabilities" = {
      schema = "/common/criteria/src/vulnerabilities/schema.json";
      targets = ["/common/criteria/src/vulnerabilities/data.yaml"];
    };
  };
}
