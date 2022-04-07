# https://github.com/fluidattacks/makes
{
  lintWithAjv = {
    "common/criteria/compliance" = {
      schema = "/makes/foss/modules/common/criteria/src/compliance/schema.json";
      targets = ["/makes/foss/modules/common/criteria/src/compliance/data.yaml"];
    };
    "common/criteria/requirements" = {
      schema = "/makes/foss/modules/common/criteria/src/requirements/schema.json";
      targets = ["/makes/foss/modules/common/criteria/src/requirements/data.yaml"];
    };
    "common/criteria/vulnerabilities" = {
      schema = "/makes/foss/modules/common/criteria/src/vulnerabilities/schema.json";
      targets = ["/makes/foss/modules/common/criteria/src/vulnerabilities/data.yaml"];
    };
  };
}
