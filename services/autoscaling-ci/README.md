# Setting up the Bastion

0. Launch a very **small EC2 instance**
0. install **docker**
0. install **docker-machine**
0. install **gitlab-runner** (it's in ubuntu's apt)
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
  volumes = ["/var/run/docker.sock:/var/run/docker.sock"]
```

And for security reasons:

```toml
# ...
[runners.machine]
  # ...
  MaxBuilds = 1
```

**MaxBuilds** 1 will make the gitlab-runner start the machine,
run 1 job,
and kill the machine.

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
