---
slug: fuzzing-sudo/
title: Sudo Heap Overflow CVE-2021-3156
date: 2021-02-01
category: attacks
subtitle: Replicating CVE-2021-3156 with AFL
tags: fuzzing, vulnerability, hacking, exploit, discovery
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330881/blog/fuzzing-sudo/cover_g2rbr6.webp
alt: Photo by Shannon Litt on Unsplash
description: In this article we will be able to reproduce the bug described
  on CVE-2021-3156 using fuzzing.
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  Fuzzing, Ethical Hacking, Pentesting, CVE-2021-3156
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSWP, OSCP, CHFI
about2: We don't need the key, we'll break in — RATM
source: https://unsplash.com/photos/XeFXUyZR-aE
---

On January 26 of 2021, Qualys
[published](https://blog.qualys.com/vulnerabilities-research/2021/01/26/cve-2021-3156-heap-based-buffer-overflow-in-sudo-baron-samedit)
a new vulnerability discovered on `sudo`, a tool used to perform actions
as other users (most commonly as `root`) on Linux-based systems.

Although Qualys provided a very good
[analysis](https://www.qualys.com/2021/01/26/cve-2021-3156/baron-samedit-heap-based-overflow-sudo.txt)
of the vulnerability, they didn’t state how they found it.

In this post, we will show a way to discover this kind of bugs using
[AFL++](https://aflplus.plus/), a community-fork of [American Fuzzy
Lop](https://lcamtuf.coredump.cx/afl/), a
[fuzzer](../fuzzing-forallsecure) that uses compile-time instrumentation
and genetic algorithms to find, among other things, security bugs.

## Preparing the environment

First, we need to install `AFL`. You just have to clone the
[repo](https://github.com/AFLplusplus/AFLplusplus) and follow the
instructions. The only necessary change I made was to specify a version
for the `libstdc++-dev` package. It needs to be the same as the `gcc`
compiler on your system:

``` bash
$ git clone https://github.com/AFLplusplus/AFLplusplus.git
$ cd AFLplusplus/
$ gcc --version
gcc (Debian 10.2.1-6) 10.2.1 20210110
Copyright (C) 2020 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
$ sudo apt install build-essential python3-dev automake flex bison libglib2.0-dev libpixman-1-dev clang python3-setuptools clang llvm llvm-dev libstdc++-10-dev
$ make distrib
$ sudo make install
```

And check the installation with:

``` bash
$ afl-gcc --version
afl-cc ++3.01a by Michal Zalewski, Laszlo Szekeres, Marc Heuse - mode: GCC-GCC
gcc (Debian 10.2.1-6) 10.2.1 20210110
Copyright (C) 2020 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

Now, we need to [download](https://www.sudo.ws/download.html) one of the
affected versions of `sudo`. We will use `1.9.5p1`.

``` bash
wget -c https://www.sudo.ws/dist/sudo-1.9.5p1.tar.gz
tar xzf sudo-1.9.5p1.tar.gz
```

That’s it, we have everything we need\!

## Patching sudo for fuzzing purposes

`AFL` uses instrumented fuzzing only on binaries built with their
compilers. Instrumented mode helps `AFL` perform coverage-guided fuzzing
and generate mutating input based on the measured behavior of previous
payloads.

However, `AFL` will expect parameters from the standard input and files
[only](https://groups.google.com/u/1/g/afl-users/c/ZBWq0LdHBzw/m/zBlo7q9LBAAJ).

`sudo` uses command-line arguments, which is not compatible with `AFL`.
However, there is a
[way](https://github.com/AFLplusplus/AFLplusplus/tree/stable/utils/argv_fuzzing)
provided by `AFL` to fuzz that kind of binaries: A `C` header that
converts a standard input payload to `argv[]` parameters.

To do that, we just need to:

- Copy the `AFLplusplus/utils/argv_fuzzing/argv-fuzz-inl.h` file to
  the main source of `sudo`.

- Modify the `main()` function of `sudo` to call the `AFL_INIT_ARGV()`
  macro.

<!-- end list -->

``` bash
~/sudo-1.9.5p1$ cp ../AFLplusplus/utils/argv_fuzzing/argv-fuzz-inl.h src/
```

``` diff
diff -urN sudo-1.9.5p1.orig/src/sudo.c sudo-1.9.5p1/src/sudo.c
--- sudo-1.9.5p1.orig/src/sudo.c    2021-01-09 15:12:16.000000000 -0500
+++ sudo-1.9.5p1/src/sudo.c 2021-02-01 09:20:58.481966614 -0500
@@ -65,6 +65,7 @@
 #include "sudo.h"
 #include "sudo_plugin.h"
 #include "sudo_plugin_int.h"
+#include "argv-fuzz-inl.h"

 /*
  * Local variables
@@ -149,6 +150,7 @@
 int
 main(int argc, char *argv[], char *envp[])
 {
+    AFL_INIT_ARGV();
     int nargc, status = 0;
     char **nargv, **env_add, **user_info;
     char **command_info = NULL, **argv_out = NULL, **user_env_out = NULL;
```

This will work by converting all the expected `argv[]` array from
standard input with parameters separated by a `\0` byte and terminating
the array with a `\0\0`.

We also need to disable the `sudo` password prompt; otherwise, the
fuzzing will hang.

``` diff
diff -urN sudo-1.9.5p1.orig/plugins/sudoers/auth/sudo_auth.c sudo-1.9.5p1/plugins/sudoers/auth/sudo_auth.c
--- sudo-1.9.5p1.orig/plugins/sudoers/auth/sudo_auth.c  2020-12-16 20:33:43.000000000 -0500
+++ sudo-1.9.5p1/plugins/sudoers/auth/sudo_auth.c   2021-02-01 09:24:36.476083963 -0500
@@ -260,6 +260,8 @@
      debug_return_int(-1);
     }

+    return 0;
+
     /* Enable suspend during password entry. */
     sigemptyset(&sa.sa_mask);
     sa.sa_flags = SA_RESTART;
```

Now, we can build our patched `sudo`. As it needs to be built with `AFL`
compilers, we must overwrite the `CC` environment variable. We may also
want to enable debugging symbols, and finally we should install it on a
isolated path so we can safely remove it when we finish our fuzzing
session. We can do that by issuing:

``` bash
CFLAGS="-g" LDFLAGS="-g" CC=afl-clang-fast ./configure --prefix=/fuzz/sudo
make
sudo make install
```

This will install our modified `sudo` on `/fuzz/sudo`. To check that our
installation worked, along with the patches, just type:

``` bash
echo -ne "sudo\0id\0\0" | /fuzz/sudo/bin/sudo
uid=0(root) gid=0(root) groups=0(root)
```

Great, now it’s fuzzing time\!

## Fuzzing sudo

When using `AFL`, I recommend having a separate directory on which you
can store the inputs and outputs for each fuzzed binary. I will create
mine at `$HOME/fuzz/sudo`.

``` bash
~/fuzz$ mkdir -p sudo/{input,output}
```

The `output` directory will be on where `AFL` will store the fuzzing
state. As this directory will be extensively written to, it is
recommended to use a RAM-based filesystem to improve performance and
avoid damaging `SSD` disks.

``` bash
~/fuzz/sudo$ sudo mount -t tmpfs tmpfs output
```

In the `input` directory, we will create initial payloads for `sudo`:

``` bash
~/fuzz/sudo$ echo -ne "sudo\0id\0\0" > input/payload1
~/fuzz/sudo$ echo -ne "sudoedit\0id\0\0" > input/payload2
```

Fuzzing is CPU-intensive, but you can use parallel fuzzing with `AFL`. I
used an 8-core PC and launched a `Master` `AFL` instance:

``` bash
~/fuzz/sudo$ afl-fuzz -i input/ -o output/ -M fuzz01 /fuzz/sudo/bin/sudo
```

And launched 6 `Slave` instances on different consoles:

``` bash
~/fuzz/sudo$ afl-fuzz -i input/ -o output/ -S fuzz02 /fuzz/sudo/bin/sudo
~/fuzz/sudo$ afl-fuzz -i input/ -o output/ -S fuzz03 /fuzz/sudo/bin/sudo
~/fuzz/sudo$ afl-fuzz -i input/ -o output/ -S fuzz04 /fuzz/sudo/bin/sudo
~/fuzz/sudo$ afl-fuzz -i input/ -o output/ -S fuzz05 /fuzz/sudo/bin/sudo
~/fuzz/sudo$ afl-fuzz -i input/ -o output/ -S fuzz06 /fuzz/sudo/bin/sudo
```

It looked like this:

<div class="imgblock">

![Parallel
Fuzzing](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330879/blog/fuzzing-sudo/parallel1_dz7xvm.webp)

</div>

And just after a few minutes of fuzzing, one of the slaves showed 3
crashes\!

<div class="imgblock">

![Parallel
Fuzzing](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330879/blog/fuzzing-sudo/crash1_ylqtwu.webp)

</div>

You can find here the payloads that caused the crashes:

``` bash
~/fuzz/sudo$ ls output/fuzz03/crashes/id\:00000*
4 output/fuzz03/crashes/id:000000,sig:06,src:000002+000209,time:276568,op:splice,rep:2
4 output/fuzz03/crashes/id:000001,sig:06,src:000125,time:404770,op:havoc,rep:8
4 output/fuzz03/crashes/id:000002,sig:06,src:000305,time:1623276,op:arith8,pos:20,val:-24
```

If we examine the contents of these payloads, we can see that they all
invoked `sudoedit` with the `-s` and `-i` flags. `AFL` mutated the
original input payloads and eventually triggered the bug found by
Qualys.

<div class="imgblock">

![Crash
payloads](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330878/blog/fuzzing-sudo/vuln1_vdlsma.webp)

</div>

We can also replicate the crash by simply passing the offending payloads
to our `sudo`:

``` bash
~/fuzz/sudo$ /fuzz/sudo/bin/sudo < output/fuzz03/crashes/id:000000,sig:06,src:000002+000209,time:276568,op:splice,rep:2
malloc(): invalid size (unsorted)
Aborted
```

And you can use `GDB` to start the exploitation process:

<div class="imgblock">

![GDB](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330880/blog/fuzzing-sudo/gdb1_vzpedo.webp)

</div>

## Conclusion

It is easy to find crashes on software using `AFL` if you have the
source code. What is unbelievable is that it took 10 years for a bug
like this to be found on `sudo`\!
