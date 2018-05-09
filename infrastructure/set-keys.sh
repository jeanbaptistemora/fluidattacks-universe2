
curl --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_S3_ACCESS_KEY" --form "value=$(terraform output fis3integrationID)"
curl --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_CLOUDWATCH_ACCESS_KEY" --form "value=$(terraform output cloudwatchID)"
curl --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_DYNAMODB_ACCESS_KEY" --form "value=$(terraform output fluidintegratesdynamoID)"
curl --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FW_AWS_ACCESS_KEY_ID" --form "value=$(terraform output fws3userID)"
curl --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_S3_SECRET_KEY" --form "value=$(terraform output fis3integrationSECRET)"
curl --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_CLOUDWATCH_SECRET_KEY" --form "value=$(terraform output cloudwatchSECRET)"
curl --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_DYNAMODB_SECRET_KEY" --form "value=$(terraform output fluidintegratesdynamoSECRET)"
curl --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FW_AWS_SECRET_ACCESS_KEY" --form "value=$(terraform output fws3userSECRET)"
