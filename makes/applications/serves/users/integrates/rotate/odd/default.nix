{ servesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path servesPkgs;
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
  name = "serves-users-integrates-rotate-odd";
  product = "serves";
  target = "serves/users/integrates/terraform";
  secretsPath = "serves/secrets/production.yaml";
  productionKeys = {
    "aws_iam_access_key.integrates-prod-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "INTEGRATES_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "integrates-prod-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "integrates-prod-secret-key-1";
        };
      };
    };
  };
  developmentKeys = {
    "aws_iam_access_key.integrates-dev-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "INTEGRATES_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "integrates-dev-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "integrates-dev-secret-key-1";
        };
      };
    };
  };
in
makeEntrypoint {
  arguments = {
    envProduct = product;
    envSecretsPath = secretsPath;
  };
  inherit name;
  searchPaths = {
    envPaths = [
      servesPkgs.curl
      servesPkgs.jq
      (userRotateKeys {
        name = "userRotateKeysProduction";
        inherit product;
        inherit target;
        inherit secretsPath;
        keys = productionKeys;
      })
      (userRotateKeys {
        name = "userRotateKeysDevelopment";
        inherit product;
        inherit target;
        inherit secretsPath;
        keys = developmentKeys;
      })
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/serves/users/integrates/rotate/entrypoint.sh";
}
