
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_S3_ACCESS_KEY" --form "value=$(terraform output fis3integrationID)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_CLOUDWATCH_ACCESS_KEY" --form "value=$(terraform output cloudwatchID)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_DYNAMODB_ACCESS_KEY" --form "value=$(terraform output fluidintegratesdynamoID)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FW_AWS_ACCESS_KEY_ID" --form "value=$(terraform output fws3userID)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_S3_SECRET_KEY" --form "value=$(terraform output fis3integrationSECRET)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_CLOUDWATCH_SECRET_KEY" --form "value=$(terraform output cloudwatchSECRET)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_DYNAMODB_SECRET_KEY" --form "value=$(terraform output fluidintegratesdynamoSECRET)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FW_AWS_SECRET_ACCESS_KEY" --form "value=$(terraform output fws3userSECRET)" > /dev/null
