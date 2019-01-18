apt-get update
apt-get install -y awscli

mkdir ~/.aws

echo "[default]" > ~/.aws/credentials
echo "aws_access_key_id=$(vault read -field=aws_s3_access_key secret/serves)" >> ~/.aws/credentials
echo "aws_secret_access_key=$(vault read -field=aws_s3_secret_key secret/serves)" >> ~/.aws/credentials

echo "[default]" > ~/.aws/config
echo "region=$(vault read -field=aws_s3_default_region secret/serves)" >> ~/.aws/config
echo "output=json" >> ~/.aws/config
