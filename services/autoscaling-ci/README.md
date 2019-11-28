# Setting up the Bastion

0. Launch a **t3.small EC2 instance** with
   **ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-20191002 (ami-04b9e92b5572fa0d1)** AMI
0. install **docker** (https://docs.docker.com/install/linux/docker-ce/ubuntu/)
0. install **docker-machine** (https://docs.docker.com/machine/install-machine/)
0. install **gitlab-runner** (https://docs.gitlab.com/runner/install/linux-repository.html)
0. take the **autoscaling-ci** user credentials (ID and Secret)
0. replace all **----REPLACE-ME----** parts in the local *config.toml*
   that you'll find in this directory
0. register two runners in **docker+machine** type and grab their **token**s
   (you'll find them in Bastion's */etc/gitlab-runner/config.toml*)
0. fusion the local *config.toml* with Bastion's */etc/gitlab-runner/config.toml*,
   (just preserve the tokens that you got while registering the runners)

# Control variables

```toml
limit      = max number of machines spawned by the bastion
concurrent = max number of machines running jobs at a same time
IdleTime   = Time (in seconds) for machine to be in Idle state before it is removed
IdleCount  = Number of machines, that need to be created and waiting in Idle state
MaxBuilds  = Builds count after which machine will be removed
```

# Rules

0. The **gitlab-runner** goal is to keep `limit <= concurrent + idle`
0. Set IdleCount to the max number of parallel jobs run in an Integration pipeline
0. set the spot instance purchase to the maximum alive time

It's a good idea to set concurrent to something really high,
and just control limit and idle

# Docker in Docker

To enable it append the following in the *config.toml*

```toml
# ...
[runners.docker]
  # ...
  privileged = true
  volumes = [
    # Let the job's Docker see the job's cloned repository which is in Host's filesystem
    "/builds:/builds",
    # Let the job's Docker use the Daemon of the Host
    #   because the job's Docker does not have the hardware, the Host does
    "/var/run/docker.sock:/var/run/docker.sock"
  ]
```

And for security reasons:

```toml
# ...
[runners.machine]
  # ...
  MaxBuilds = 1
```

# IO1 Volumes

To enable it append the following in the *config.toml*

```toml
# ...
[runners.machine]
  # ...
  MachineOptions = [
    # ...
    "amazonec2-volume-type=io1",
    "amazonec2-volume-iops=800",  # At much 50 times root-size GiB
    "amazonec2-root-size=16"
    # ...
  ]
```

**MaxBuilds** 1 will make the gitlab-runner start the machine,
run 1 job,
and kill the machine.

Overwrite the docker-machine binary in the Bastion with:

https://github.com/kamadorueda/machine/blob/master/bin/docker-machine

If you need to perform more changes,
clone the official repository,
make changes
install Moby dev environment (go, compilers and docker)
and run 'make build' to compile your modified binary

# SPOT instances

To enable it append the following in the *config.toml*

```toml
# ...
[runners.machine]
  # ...
  MachineOptions = [
    # ...
    "amazonec2-request-spot-instance=true",
    "amazonec2-spot-price=",
    "amazonec2-block-duration-minutes=360",
  ]
```

Notice that this will save costs but will cause some system failures.
This happens because the spot instance is removed after
*amazonec2-block-duration-minutes*,
so jobs run near the end of the instance lifetime will be killed
