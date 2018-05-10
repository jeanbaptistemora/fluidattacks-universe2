
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_S3_ACCESS_KEY" --form "value=$(cat fis3integrationID.txt)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_CLOUDWATCH_ACCESS_KEY" --form "value=$(cat cloudwatchID.txt)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_DYNAMODB_ACCESS_KEY" --form "value=$(cat fluidintegratesdynamoID.txt)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FW_AWS_ACCESS_KEY_ID" --form "value=$(cat fws3userID.txt)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_S3_SECRET_KEY" --form "value=$(cat fis3integrationSECRET.txt)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_CLOUDWATCH_SECRET_KEY" --form "value=$(cat cloudwatchSECRET.txt)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FI_AWS_DYNAMODB_SECRET_KEY" --form "value=$(cat fluidintegratesdynamoSECRET.txt)" > /dev/null
curl -s --request PUT --header "PRIVATE-TOKEN: $FS_GITLAB_API_SECRET" "https://gitlab.com/api/v4/groups/fluidsignal/variables/FW_AWS_SECRET_ACCESS_KEY" --form "value=$(cat fws3userSECRET.txt)" > /dev/null
