{ servesPkgs
, path
, ...
} @ _:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-airs-rotate-even";
  product = "serves";
  target = "serves/users/airs/terraform";
  secrets_path = "serves/secrets/production.yaml";
  gitlab_project_id = "20741933";
  keys = {
    "aws_iam_access_key.web-prod-key-2" = {
      id = {
        gitlab = {
          id = "AIRS_PROD_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = true;
        };
        output = {
          id = "web-prod-secret-key-id-2";
        };
      };
      secret = {
        gitlab = {
          id = "AIRS_PROD_AWS_SECRET_ACCESS_KEY";
          masked = true;
          protected = true;
        };
        output = {
          id = "web-prod-secret-key-2";
        };
      };
    };
    "aws_iam_access_key.web-dev-key-2" = {
      id = {
        gitlab = {
          id = "AIRS_DEV_AWS_ACCESS_KEY_ID";
          masked = true;
          protected = false;
        };
        output = {
          id = "web-dev-secret-key-id-2";
        };
      };
      secret = {
        gitlab = {
          id = "AIRS_DEV_AWS_SECRET_ACCESS_KEY";
          masked = true;
          protected = false;
        };
        output = {
          id = "web-dev-secret-key-2";
        };
      };
    };
  };
}
