{ inputs
, makeSearchPaths
, makeTemplate
, ...
}:
{
  dev = {
    integratesBack = {
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
        (makeSearchPaths {
          pythonPackage = [
            "$PWD/integrates"
            "$PWD/integrates/back/src"
          ];
        })
      ];
    };
  };
}
