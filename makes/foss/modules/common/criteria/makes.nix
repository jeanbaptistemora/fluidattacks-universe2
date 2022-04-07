# https://github.com/fluidattacks/makes
{
  lintWithAjv = {
    "makes/criteria/compliance" = {
      schema = "/makes/foss/modules/common/criteria/src/compliance/schema.json";
      targets = ["/makes/foss/modules/common/criteria/src/compliance/data.yaml"];
    };
    "makes/criteria/requirements" = {
      schema = "/makes/foss/modules/common/criteria/src/requirements/schema.json";
      targets = ["/makes/foss/modules/common/criteria/src/requirements/data.yaml"];
    };
    "makes/criteria/vulnerabilities" = {
      schema = "/makes/foss/modules/common/criteria/src/vulnerabilities/schema.json";
      targets = ["/makes/foss/modules/common/criteria/src/vulnerabilities/data.yaml"];
    };
  };
}
