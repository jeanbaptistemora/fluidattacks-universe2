{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "makes-users-makes-rotate-even";
  product = "makes";
  target = "makes/applications/makes/users/makes/src/terraform";
  keys = {
    "aws_iam_access_key.dev-key-2" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "MAKES_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "dev-secret-key-id-2";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "MAKES_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "dev-secret-key-2";
        };
      };
    };
  };
}
