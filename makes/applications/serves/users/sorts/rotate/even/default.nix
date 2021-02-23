{ servesPkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-sorts-rotate-even";
  product = "serves";
  target = "serves/users/sorts/terraform";
  keys = {
    "aws_iam_access_key.sorts_prod_key-2" = {
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
          id = "sorts_prod_access_key-2";
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
          id = "sorts_prod_secret_key-2";
        };
      };
    };
    "aws_iam_access_key.sorts_dev_key-2" = {
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
          id = "sorts_dev_access_key-2";
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
          id = "sorts_dev_secret_key-2";
        };
      };
    };
  };
}
