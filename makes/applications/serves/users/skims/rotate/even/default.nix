{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "serves-users-skims-rotate-even";
  product = "serves";
  target = "serves/users/skims/terraform";
  keys = {
    "aws_iam_access_key.skims_prod_key-2" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SKIMS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "skims_prod_secret_key_id-2";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SKIMS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "skims_prod_secret_key-2";
        };
      };
    };
    "aws_iam_access_key.skims_dev_key-2" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SKIMS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "skims_dev_secret_key_id-2";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SKIMS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "skims_dev_secret_key-2";
        };
      };
    };
  };
}
