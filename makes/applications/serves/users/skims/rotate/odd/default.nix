{ servesPkgs
, path
, ...
} @ _:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-skims-rotate-odd";
  product = "serves";
  target = "serves/users/skims/terraform";
  keys = {
    "aws_iam_access_key.skims_prod_key-1" = {
      id = {
        gitlab = {
          project_ids = [ "20741933" ];
          id = "SKIMS_PROD_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = true;
        };
        output = {
          id = "skims_prod_secret_key_id-1";
        };
      };
      secret = {
        gitlab = {
          project_ids = [ "20741933" ];
          id = "SKIMS_PROD_AWS_SECRET_ACCESS_KEY";
          masked = true;
          protected = true;
        };
        output = {
          id = "skims_prod_secret_key-1";
        };
      };
    };
    "aws_iam_access_key.skims_dev_key-1" = {
      id = {
        gitlab = {
          project_ids = [ "20741933" ];
          id = "SKIMS_DEV_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = false;
        };
        output = {
          id = "skims_dev_secret_key_id-1";
        };
      };
      secret = {
        gitlab = {
          project_ids = [ "20741933" ];
          id = "SKIMS_DEV_AWS_SECRET_ACCESS_KEY";
          masked = true;
          protected = false;
        };
        output = {
          id = "skims_dev_secret_key-1";
        };
      };
    };
  };
}
