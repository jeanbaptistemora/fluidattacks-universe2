{ servesPkgs
, path
, ...
} @ _:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-asserts-rotate-odd";
  product = "serves";
  target = "serves/users/asserts/terraform";
  keys = {
    "aws_iam_access_key.asserts-prod-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "ASSERTS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "asserts-prod-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "ASSERTS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "asserts-prod-secret-key-1";
        };
      };
    };
    "aws_iam_access_key.asserts-dev-key-1" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "ASSERTS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "asserts-dev-secret-key-id-1";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "ASSERTS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "asserts-dev-secret-key-1";
        };
      };
    };
  };
}
