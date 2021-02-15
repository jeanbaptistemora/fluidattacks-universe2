{ servesPkgs
, path
, ...
} @ _:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-airs-rotate-odd";
  product = "serves";
  target = "serves/users/airs/terraform";
  secrets_path = "serves/secrets/production.yaml";
  keys = {
    "aws_iam_access_key.web-prod-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "AIRS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "web-prod-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "AIRS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "web-prod-secret-key-1";
        };
      };
    };
    "aws_iam_access_key.web-dev-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "AIRS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "web-dev-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "AIRS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "web-dev-secret-key-1";
        };
      };
    };
  };
}
