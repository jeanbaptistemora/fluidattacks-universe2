# https://github.com/fluidattacks/makes
{
  lintWithAjv = {
    "makes/criteria/compliance" = {
      schema = "/makes/foss/modules/makes/criteria/src/compliance/schema.json";
      targets = [ "/makes/foss/modules/makes/criteria/src/compliance/data.yaml" ];
    };
    "makes/criteria/requirements" = {
      schema = "/makes/foss/modules/makes/criteria/src/requirements/schema.json";
      targets = [ "/makes/foss/modules/makes/criteria/src/requirements/data.yaml" ];
    };
    "makes/criteria/vulnerabilities" = {
      schema = "/makes/foss/modules/makes/criteria/src/vulnerabilities/schema.json";
      targets = [ "/makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml" ];
    };
  };
}
