{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "serves-users-forces-rotate-odd";
  product = "serves";
  target = "serves/users/forces/terraform";
  keys = {
    "aws_iam_access_key.forces_prod_key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "FORCES_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "forces_prod_secret_key_id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "FORCES_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "forces_prod_secret_key-1";
        };
      };
    };
    "aws_iam_access_key.forces_dev_key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "FORCES_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "forces_dev_secret_key_id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "FORCES_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "forces_dev_secret_key-1";
        };
      };
    };
  };
}
