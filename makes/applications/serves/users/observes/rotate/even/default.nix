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
  keys = {
    "aws_iam_access_key.prod-key-2" = {
      id = {
        gitlab = {
          project_ids = [ "20741933" ];
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
          project_ids = [ "20741933" ];
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
          project_ids = [ "20741933" ];
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
          project_ids = [ "20741933" ];
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
