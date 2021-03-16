{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "serves-users-skims-rotate-odd";
  product = "serves";
  target = "makes/applications/serves/users/skims/src/terraform";
  keys = {
    "aws_iam_access_key.skims_prod_key-1" = {
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
          id = "skims_prod_secret_key_id-1";
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
          id = "skims_prod_secret_key-1";
        };
      };
    };
    "aws_iam_access_key.skims_dev_key-1" = {
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
          id = "skims_dev_secret_key_id-1";
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
          id = "skims_dev_secret_key-1";
        };
      };
    };
  };
}
