# Streamer infrastructure

This is the Extract component of an infrastructure stats ET&L.

## Getting started

First create a JSON file with your credentials:
```
{
    "AWS_ACCESS_KEY_ID": "123",
    "AWS_SECRET_ACCESS_KEY": "456",
    "AWS_DEFAULT_REGION": "us-east-1"
}
```

Then run the streamer:

```
streamer-infrastructure --auth credentials.json
```
