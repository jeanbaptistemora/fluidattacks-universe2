{ nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
  name = "makes-users-integrates-rotate-even";
  product = "makes";
  target = "makes/applications/makes/users/integrates/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/production.yaml";
  productionKeys = {
    "aws_iam_access_key.integrates-prod-key-2" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
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
            api_token = "PRODUCT_API_TOKEN";
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
  developmentKeys = {
    "aws_iam_access_key.integrates-dev-key-2" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
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
            api_token = "PRODUCT_API_TOKEN";
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
  };
  inherit name;
  searchPaths = {
    envPaths = [
      nixpkgs.curl
      nixpkgs.jq
      (userRotateKeys {
        name = "user-rotate-keys-production";
        inherit product;
        inherit target;
        inherit secretsPath;
        keys = productionKeys;
      })
      (userRotateKeys {
        name = "user-rotate-keys-development";
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
  template = path "/makes/applications/makes/users/integrates/rotate/entrypoint.sh";
}
