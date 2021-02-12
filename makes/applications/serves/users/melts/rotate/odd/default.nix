{ servesPkgs
, path
, ...
} @ _:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-melts-rotate-odd";
  product = "serves";
  target = "serves/users/melts/terraform";
  gitlab_project_id = "20741933";
  keys = {
    "aws_iam_access_key.melts-prod-key-1" = {
      id = {
        gitlab = {
          id = "MELTS_PROD_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = true;
        };
        output = {
          id = "prod-secret-key-id-1";
        };
      };
      secret = {
        gitlab = {
          id = "MELTS_PROD_AWS_SECRET_ACCESS_KEY";
          masked = true;
          protected = true;
        };
        output = {
          id = "prod-secret-key-1";
        };
      };
    };
    "aws_iam_access_key.melts-dev-key-1" = {
      id = {
        gitlab = {
          id = "MELTS_DEV_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = false;
        };
        output = {
          id = "dev-secret-key-id-1";
        };
      };
      secret = {
        gitlab = {
          id = "MELTS_DEV_AWS_SECRET_ACCESS_KEY";
          masked = true;
          protected = false;
        };
        output = {
          id = "dev-secret-key-1";
        };
      };
    };
  };
}
