{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "serves-users-sorts-rotate-odd";
  product = "serves";
  target = "makes/applications/serves/users/sorts/src/terraform";
  keys = {
    "aws_iam_access_key.sorts_prod_key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SORTS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "sorts_prod_access_key-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SORTS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "sorts_prod_secret_key-1";
        };
      };
    };
    "aws_iam_access_key.sorts_dev_key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SORTS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "sorts_dev_access_key-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SORTS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "sorts_dev_secret_key-1";
        };
      };
    };
  };
}
