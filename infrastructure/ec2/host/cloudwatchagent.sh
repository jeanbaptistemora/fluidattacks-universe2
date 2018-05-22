#/bin/bash
sudo apt-get install -y unzip
mkdir /tmp/AmazonCloudWatchAgent
cd /tmp/AmazonCloudWatchAgent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/linux/amd64/latest/AmazonCloudWatchAgent.zip
unzip AmazonCloudWatchAgent.zip
sudo ./install.sh
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/tmp/cloudwatchagent-conf.json -s
