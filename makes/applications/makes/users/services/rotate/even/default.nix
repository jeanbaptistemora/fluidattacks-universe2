{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "makes-users-services-rotate-even";
  product = "makes";
  target = "makes/applications/makes/users/services/src/terraform";
  keys = {
    "aws_iam_access_key.continuous-prod-key-2" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "SERVICES_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
          {
            api_token = "SERVICES_API_TOKEN";
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
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "SERVICES_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
          {
            api_token = "SERVICES_API_TOKEN";
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
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "SERVICES_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
          {
            api_token = "SERVICES_API_TOKEN";
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
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "SERVICES_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
          {
            api_token = "SERVICES_API_TOKEN";
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
