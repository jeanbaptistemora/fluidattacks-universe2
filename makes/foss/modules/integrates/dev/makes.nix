{ inputs
, makeTemplate
, ...
}:
{
  dev = {
    integratesBack = {
      pythonPackage = [
        "integrates"
        "integrates/back/src"
      ];
      source = [
        (makeTemplate {
          name = "integrates-dev";
          replace = {
            __argIntegratesBackEnv__ = inputs.product.integrates-back-env;
          };
          template = ''
            require_env_var INTEGRATES_DEV_AWS_ACCESS_KEY_ID
            require_env_var INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY
            source __argIntegratesBackEnv__ dev
          '';
        })
      ];
    };
  };
}
