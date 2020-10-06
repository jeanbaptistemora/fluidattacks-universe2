# Computes

A processing pool micro-service that receives tasks definitions and ensure
they are executed successfully in the cloud.

Currently you can execute any `./build.sh` command here.

It's guaranteed that if the job runs locally, it'll run on the cloud (thanks to Nix).

Just make sure you propagate the required secrets as environment variables as that is the only impurity.

# Using

There is a helper in common.sh to simplify the process,
below you'll find its rationale.

In order to execute `./build.sh test_job "${arg1}" "${arg2}"` on the cloud:

1. Create a job definition:

    ```sh
    arg1='123'
    arg2='456'
    definition=$(jq -e -n -r '{
      command: ["./build.sh", "test_job", env.arg1, env.arg2],
      environment: [
        {name: "SECRET1", value: env.SECRET1},
        {name: "SECRET2", value: env.SECRET2},
      ],
      memory: 1024,
      vcpus: 1
    }')
    ```

    Propagate the required environment variables in the `environment` section
    and pick a reasonable amount of memory (MB) and virtual CPU.

1. Login to AWS

1. Submit the job to any of the queues using the default definition, add a nice name:

    ```sh
    aws batch submit-job \
      --container-overrides "${definition}" \
      --job-name "your-job-name" \
      --job-queue 'default' \
      --job-definition 'default' \
      --retry-strategy 'attempts=1' \
      --timeout 'attemptDurationSeconds=3600' \
    ```

1. Done!

# Queues available

- **default**: A new job will wait from minutes to days before being executed.
  Jobs may be interrupted randomly.
  use many attempts and submit only short-running jobs.
- **asap**: A new job will be executed as soon as possible.
  Jobs may be interrupted randomly.
  use many attempts and submit only short-running jobs.
- **default-uninterruptible**: A new job may wait from minutes to days before being executed.
  Jobs are never interrupted but are more expensive ($$) to run.
- **asap-uninterruptible**: A new job will be executed as-soon-as-possible.
  Jobs are never interrupted but are more expensive ($$) to run.

Note that if you send all jobs to the asap queue, it will saturate anyway.

# Privileges required

```tf
statement {
  effect = "Allow"
  actions = ["batch:SubmitJob"]
  resources = [
    "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/default",
    "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/default",
    "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/default-uninterruptible",
    "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/asap",
    "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/asap-uninterruptible",
  ]
}
```

# Further work

Implement many queues to allow running high priority jobs first.
