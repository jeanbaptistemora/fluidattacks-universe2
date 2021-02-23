{ servesPkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path servesPkgs;
in
userRotateKeys {
  name = "serves-users-services-rotate-even";
  product = "serves";
  target = "serves/users/services/terraform";
  keys = {
    "aws_iam_access_key.continuous-prod-key-2" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SERVICES_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
          {
            project_id = "4603023";
            key_id = "PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "continuous-prod-secret-key-id-2";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SERVICES_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
          {
            project_id = "4603023";
            key_id = "PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "continuous-prod-secret-key-2";
        };
      };
    };
    "aws_iam_access_key.continuous-dev-key-2" = {
      id = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SERVICES_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
          {
            project_id = "4603023";
            key_id = "DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "continuous-dev-secret-key-id-2";
        };
      };
      secret = {
        gitlab = [
          {
            project_id = "20741933";
            key_id = "SERVICES_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
          {
            project_id = "4603023";
            key_id = "DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "continuous-dev-secret-key-2";
        };
      };
    };
  };
}
