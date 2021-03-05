{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "serves-users-airs-rotate-even";
  product = "serves";
  target = "serves/users/airs/terraform";
  secretsPath = "serves/secrets/production.yaml";
  keys = {
    "aws_iam_access_key.web-prod-key-2" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "AIRS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "web-prod-secret-key-id-2";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "AIRS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "web-prod-secret-key-2";
        };
      };
    };
    "aws_iam_access_key.web-dev-key-2" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "AIRS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "web-dev-secret-key-id-2";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "AIRS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "web-dev-secret-key-2";
        };
      };
    };
  };
}
