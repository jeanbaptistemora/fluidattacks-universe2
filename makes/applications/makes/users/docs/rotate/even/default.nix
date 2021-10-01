{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "makes-users-docs-rotate-even";
  product = "makes";
  target = "makes/makes/users/docs/infra";
  secretsPath = "makes/makes/secrets/prod.yaml";
  keys = {
    "aws_iam_access_key.prod_2" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "DOCS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "prod_secret_key_id_2";
        };
      };
      secret = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "DOCS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "prod_secret_key_2";
        };
      };
    };
    "aws_iam_access_key.dev_2" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "DOCS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "dev_secret_key_id_2";
        };
      };
      secret = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "DOCS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "dev_secret_key_2";
        };
      };
    };
  };
}
