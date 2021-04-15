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
  target = "makes/applications/makes/users/docs/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/production.yaml";
  keys = {
    "aws_iam_access_key.prod_2" = {
      id = {
        gitlab = [
          {
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
