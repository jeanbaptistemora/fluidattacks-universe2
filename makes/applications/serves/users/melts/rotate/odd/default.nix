{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "serves-users-melts-rotate-odd";
  product = "serves";
  target = "serves/users/melts/terraform";
  keys = {
    "aws_iam_access_key.melts-prod-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "MELTS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "prod-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "MELTS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "prod-secret-key-1";
        };
      };
    };
    "aws_iam_access_key.melts-dev-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "MELTS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "dev-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "MELTS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "dev-secret-key-1";
        };
      };
    };
  };
}
