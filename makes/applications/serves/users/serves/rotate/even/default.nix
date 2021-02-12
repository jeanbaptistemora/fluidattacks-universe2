{ servesPkgs
, path
, ...
} @ _:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-serves-rotate-even";
  product = "serves";
  target = "serves/users/serves/terraform";
  keys = {
    "aws_iam_access_key.dev-key-2" = {
      id = {
        gitlab = {
          project_ids = [ "20741933" ];
          id = "SERVES_DEV_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = false;
        };
        output = {
          id = "dev-secret-key-id-2";
        };
      };
      secret = {
        gitlab = {
          project_ids = [ "20741933" ];
          id = "SERVES_DEV_AWS_SECRET_ACCESS_KEY";
          masked = true;
          protected = false;
        };
        output = {
          id = "dev-secret-key-2";
        };
      };
    };
  };
}
