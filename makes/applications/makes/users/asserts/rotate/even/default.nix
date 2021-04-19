{ nixpkgs
, path
, ...
}:
let
  userRotateKeys = import (path "/makes/utils/user-rotate-keys") path nixpkgs;
in
userRotateKeys {
  name = "makes-users-asserts-rotate-even";
  product = "makes";
  target = "makes/applications/makes/users/asserts/src/terraform";
  keys = {
    "aws_iam_access_key.asserts-prod-key-2" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "ASSERTS_PROD_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "asserts-prod-secret-key-id-2";
        };
      };
      secret = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "ASSERTS_PROD_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = true;
          }
        ];
        output = {
          id = "asserts-prod-secret-key-2";
        };
      };
    };
    "aws_iam_access_key.asserts-dev-key-2" = {
      id = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "ASSERTS_DEV_AWS_ACCESS_KEY_ID";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "asserts-dev-secret-key-id-2";
        };
      };
      secret = {
        gitlab = [
          {
            api_token = "PRODUCT_API_TOKEN";
            project_id = "20741933";
            key_id = "ASSERTS_DEV_AWS_SECRET_ACCESS_KEY";
            masked = true;
            protected = false;
          }
        ];
        output = {
          id = "asserts-dev-secret-key-2";
        };
      };
    };
  };
}
