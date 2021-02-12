{ servesPkgs
, path
, ...
} @ _:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-observes-rotate-even";
  product = "serves";
  target = "serves/users/observes/terraform";
  gitlab_project_id = "20741933";
  keys = {
    "aws_iam_access_key.prod-key-2" = {
      id = {
        gitlab = {
          id = "OBSERVES_PROD_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = true;
        };
        output = {
          id = "prod-secret-key-id-2";
        };
      };
      secret = {
        gitlab = {
          id = "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY";
          masked = true;
          protected = true;
        };
        output = {
          id = "prod-secret-key-2";
        };
      };
    };
    "aws_iam_access_key.dev-key-2" = {
      id = {
        gitlab = {
          id = "OBSERVES_DEV_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = false;
        };
        output = {
          id = "dev-secret-key-id-2";
        };
      };
      secret = {
        gitlab = {
          id = "OBSERVES_DEV_AWS_SECRET_ACCESS_KEY";
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
