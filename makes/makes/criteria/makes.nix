# https://github.com/fluidattacks/makes
{
  lintWithAjv = {
    "makes/criteria/compliance" = {
      schema = "/makes/makes/criteria/src/compliance/schema.json";
      targets = [ "/makes/makes/criteria/src/compliance/data.yaml" ];
    };
    "makes/criteria/requirements" = {
      schema = "/makes/makes/criteria/src/requirements/schema.json";
      targets = [ "/makes/makes/criteria/src/requirements/data.yaml" ];
    };
    "makes/criteria/vulnerabilities" = {
      schema = "/makes/makes/criteria/src/vulnerabilities/schema.json";
      targets = [ "/makes/makes/criteria/src/vulnerabilities/data.yaml" ];
    };
  };
}
