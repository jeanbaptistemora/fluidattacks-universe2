{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "makes-users-airs-rotate-odd";
  product = "makes";
  target = "makes/applications/makes/users/airs/src/terraform";
  secretsPath = "makes/makes/secrets/prod.yaml";
  keys = {
    "aws_iam_access_key.web-prod-key-1" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "AIRS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "web-prod-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "AIRS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "web-prod-secret-key-1";
        };
      };
    };
    "aws_iam_access_key.web-dev-key-1" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "AIRS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "web-dev-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "AIRS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "web-dev-secret-key-1";
        };
      };
    };
  };
}
