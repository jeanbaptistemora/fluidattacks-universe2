{ servesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path servesPkgs;
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
  name = "serves-users-integrates-rotate-even";
  product = "serves";
  target = "serves/users/integrates/terraform";
  secretsPath = "serves/secrets/production.yaml";

  # Production
  productionName = "serves-users-integrates-rotate-even-production";
  productionKeys = {
    "aws_iam_access_key.integrates-prod-key-2" = {
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
          id = "integrates-prod-secret-key-id-2";
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
          id = "integrates-prod-secret-key-2";
        };
      };
    };
  };

  # Development
  developmentName = "serves-users-integrates-rotate-even-development";
  developmentKeys = {
    "aws_iam_access_key.integrates-dev-key-2" = {
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
          id = "integrates-dev-secret-key-id-2";
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
          id = "integrates-dev-secret-key-2";
        };
      };
    };
  };
in
makeEntrypoint {
  arguments = {
    envProduct = product;
    envSecretsPath = secretsPath;
    envuserRotateKeysProduction = "${userRotateKeys {
      name = productionName;
      inherit product;
      inherit target;
      inherit secretsPath;
      keys = productionKeys;
    }}/bin/${productionName}";
    envuserRotateKeysDevelopment = "${userRotateKeys {
      name = developmentName;
      inherit product;
      inherit target;
      inherit secretsPath;
      keys = developmentKeys;
    }}/bin/${developmentName}";
  };
  inherit name;
  searchPaths = {
    envPaths = [
      servesPkgs.curl
      servesPkgs.jq
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/serves/users/integrates/rotate/entrypoint.sh";
}
