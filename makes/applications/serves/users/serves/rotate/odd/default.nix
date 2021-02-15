{ servesPkgs
, path
, ...
} @ _:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-serves-rotate-odd";
  product = "serves";
  target = "serves/users/serves/terraform";
  keys = {
    "aws_iam_access_key.dev-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SERVES_DEV_AWS_ACCESS_KEY_ID";
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
            key_id = "SERVES_DEV_AWS_SECRET_ACCESS_KEY";
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
