---
slug: infinite-monkey-fuzzer/
title: The Infinite Monkey Fuzzer
date: 2018-02-12
category: attacks
subtitle: Fuzz testing using American Fuzzy Lop
tags: fuzzing, application, hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330921/blog/infinite-monkey-fuzzer/cover_a1u7uj.webp
alt: Photo by su fu on Unsplash
description: In this blog post, we are focused on how to perform basic fuzz
  attacks on desktop Linux C applications using American Fuzzy Lop.
keywords: Fuzzing, Attack, AFL, Vulnerability, Security, Application, Hacking,
  Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/N-6mnzmVljA
---

In our [last entry](../fuzzy-bugs-online/), we argued that fuzzing is
both dumb and surprising.
In this article,
we’ll continue exploring the possibilities of fuzzing.
This time though, we’ll focus on
desktop application fuzzing,
specifically UNIX applications written in C.

When developing in `C`, you usually have to handle memory issues
yourself. This makes your program very fast compared to languages like
`Java`. But at the same time this can lead to numerous kinds of
memory-access errors v.g. heap and stack
overflows.[<sup>\[1\]</sup>](#r1%20)

## The woes of fuzzing

Recall that in our last article we ran a very simple-minded kind of
fuzzing: give the fuzzer a list of inputs and it will invoke the program
with each of those inputs one at a time. Since the list was very
generic, only the most trivial inputs were successful; because it was
not random at all, there could be no surprises.

Another type of fuzzing could be by injecting random inputs: this could
lead nowhere, but it could show surprises, as we discussed in our last
entry. Some go as far as saying that [Heartbleed could have been found
with
fuzzing](https://blog.hboeck.de/archives/868-How-Heartbleed-couldve-been-found.html).

But blind, random fuzzing is usually very shallow, as was our attempted
`SQL` injection fuzzing. Such methods are \`\`very unlikely to reach
certain code paths in the tested code'' Amongst the attempts at solving
this problem we can count:

- corpus distillation

- program flow analysis

- [symbolic execution](../symbolic-execution-mortals/), and

- static analysis.

However, while these methods appear to be very promising, they tend to
be impractical in real use.[<sup>\[2\]</sup>](#r2%20)

## Down the Rabbit-Hole

[American Fuzzy Lop (`AFL`)](http://lcamtuf.coredump.cx/afl/) is a
'security-oriented brute-force fuzzer' that tries to solve these issues
with 'compile-time instrumentation' and 'genetic algorithms'. But what
the heck does all that mean?

A different approach would be to make your fuzzer aware of the file
format taken by the tested program as input, but this is rather
inconvenient. Instead, what `AFL` does is, in plain words:

1. take the source code of your app,

2. compile it in a \`\`tricked'' way,

3. run it with a good input and then

4. iteratively modifying that input until you get an error.

For example, you might start `AFL` on a program with an image of a
rabbit as input. Then the fuzzer modifies the image a little piece at a
time, feeding it back to the tested program until a hang or crash or
other unexpected behavior happens. Here you can see the sequence of
images fed into the tested program:

<div class="imgblock">

!["Fuzzed image inputs"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330933/blog/infinite-monkey-fuzzer/afl-fuzz-logo_akkh66.gif)

<div class="title">

Figure 1. Fuzzed `AFL` logo.
Via [Wikimedia](https://en.wikipedia.org/wiki/File:AFL_Fuzz_Logo.gif)

</div>

</div>

## Running AFL

The American Fuzzy Lop is primarily a white-box testing tool, so you
must have the code for the app you want to test. This is because `AFL`
needs to trick the app during compilation in a process known as
'instrumentation' so that it will allow the fuzzing process. Thus you
must compile using the included `afl-gcc`, which is a modified version
of the `GNU Compiler Collection`.

Then you should run your program with a valid, simple input: `program
input`. If that goes well, put that input file in a folder by itself.
I’ll call it `in`. Make another empty one for the results called
`out`. I’m assuming everything lives in the folder you are in right now.
Now you’re ready to run `AFL`:

**Invoking the AFL fuzzer.**

``` bash
afl-fuzz -i in -o out program input @@
```

If everything went right, then you should see this:

<div class="imgblock">

!["`AFL` interface screenshot"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330919/blog/infinite-monkey-fuzzer/scr-afl-single-677x462_muo6tm.webp)

<div class="title">

Figure 2. `AFL` main interface

</div>

</div>

Not very exciting, huh? But as long as the `total paths` indicator is
not stuck at 1, trust me, it’s doing its thing. `AFL` will continue
running until you tell it to stop by hitting `<Ctrl-C>`.

When `last uniq crash` or `last uniq hang` stops saying `` `none seen
yet'',
you have made your program crash.
`AFL `` will save the inputs that provoked the crash in the output
folder we specified.

## Fuzzing libpng - details

`libpng` is the official PNG reference library. If you’ve ever seen an
image in a web browser, you’ve been using it indirectly. It is used by
`ghostscript`, `imagemagick`, amongst many others.

As listed in its [website](http://libpng.org/pub/png/libpng.html), it
has had many bugs throughout its history. We’re interested in showing
here how to find
[CVE-2015-8126](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-8126)
which is a potential pointer overflow/underflow, using `American Fuzzy
Lop` (which is how they found it in the first place).

As it turns out, it’s not just a matter of following the generic
instructions above, because if you do:

- the fuzzer will tell you that the execution speed is slow

- a single instance of `afl-fuzz` on a single core will take a long
  time

- it won’t find anything anyway, because you need to patch `libpng`

- you need the right executable using `libpng`, namely `optipng`

So, let’s fix all these issues in the right order. Here the credit is
due to [Jakub
Wilk](https://groups.google.com/forum/#!topic/afl-users/4p3UmkpWWR0) who
originally reported the bug.

1. Apply [this
    patch](https://github.com/mirrorer/afl/blob/master/experimental/libpng_no_checksum/libpng-nocrc.patch)
    to `pngrutil.c` to `libpng-1.5.1`

2. You need to instrument `libpng` and `optipng-0.7.5` using
    `afl-clang` instead of the default `afl-gcc`. Also install `libpng`
    with `make clean all` so it doesn’t conflict with your local
    installation (which you most certainly have):

    ``` make
    CC="afl-clang" CXX="afl-clang``" ./configure --disable-shared
    make clean all
    CC="afl-clang" CXX="afl-clang``" ./configure -without-system-libpng
    make install
    ```

3. To use all `n` cores available to you, create `n` subdirectories in
    your output folder. Run `afl-fuzz` as before with the option `-M
    folder1` for the first core, and `-S folderx` for the rest. Example
    with two cores:

    ``` bash
    $ afl-fuzz -i in -o out -M core0 program input @@
    $ afl-fuzz -i in -o out -S core1 program input @@
    ```

4. Use a small `PNG` file as input, such as `not_kitty.png` included in
    `AFL`.

5. You can further speed up the process by `` `cheating''
    using a previously produced set of fuzzed images available
    here.
    Put these images in your `out `` folder.

Following the steps above, here is the optimised `afl-fuzz` running on
`libpng` and `optipng` with 4 cores:

<div class="imgblock">

!["AFL running on 4 cores"](https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,r_1,w_800/v1620330920/blog/infinite-monkey-fuzzer/anim-afl-4-cores_qegsgb.gif)

<div class="title">

Figure 3. `AFL` succesful run
([click](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330920/blog/infinite-monkey-fuzzer/anim-afl-4-cores_qegsgb.gif)
to view larger)

</div>

</div>

We see that, within a few minutes, the slave processes have made the app
hang, but not the master. The reason falls out of the scope of the
article, though; see [`AFL` performance
tips](http://lcamtuf.coredump.cx/afl/technical_details.txt).

## So what’s the bug?

OK, we made the application hang. So what? It’s not up to me to explain
it, but I will quote the essentials from the pros for the sake of
completeness.

Back then, if you called `optipng` with this
[file](https://bugs.debian.org/cgi-bin/bugreport.cgi?att=1;bug=787647;filename=crash.png;msg=3)
you’d crash it:

``` text
    $ optipng crash.png
    ** Processing: crash.png
    Warning: Can't read the input file or unexpected end of file
    24x32 pixels, 1 bit/pixel, 4 colors in palette, interlaced
    optipng: opngreduc.c:697: opng_reduce_palette_bits:
    Assertion `src_bit_depth == dest_bit_depth' failed.
    Aborted
```

The problem happens when an application uses low-bit-depth palette
mapped `PNG` data because when returning the palette it has to be copied
back to the `OS`-specific format in a potentially vulnerable way:

``` c
    for (i=0; i<num_palette; ++i) {
        bmh.palette[i][0] = tmp_palette[i].red;
        bmh.palette[i][1] = tmp_palette[i].green;
        bmh.palette[i][2] = tmp_palette[i].blue;
    }
```

And here’s the problem with that code:

`` `This is valid code according to the `PNG `` spec because
`num_palette` cannot be more than 16 in a valid `PNG`. Unfortunately in
`libpng` before the fix `num_palette` can be up to 256 with an
appropriately modified `PNG`. The overwrite above is at the high address
end of `bmh`, so it overwrites up the stack (on a typical machine) into
the call frame and pretty much gives an attacker complete control over
the application program.'' [<sup>\[3\]</sup>](#r3)

This bug was actually found using `AFL` at the time on [`Debian
Sid`](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=787647), as has
been the case for many other real-world `C` applications, even
high-profile ones like `bash`, the `X server`, `curl`, and the `Linux
kernel`. See \`AFL’s [\`\`bug-o-rama trophy
case''](http://lcamtuf.coredump.cx/afl/#bugs).

So there you have it: as promised, a more in-depth follow-up to our
[initial invitation to fuzzing](../fuzzy-bugs-online/). According to
\`AFL’s father, this technique is both very powerful and
underappreciated:

> Fuzzing is one of the most powerful and proven strategies for
> identifying security issues in real-world software; it is responsible
> for the vast majority of remote code execution and privilege
> escalation bugs found to date in security-critical
> software.[<sup>\[2\]</sup>](#r2)
>
> —  Michal Zalewski

Hopefully this article has helped to spark some curiosity and convince
you a little of that.

## References

1. [The Fuzzing Project](https://fuzzing-project.org/)

2. [American Fuzzy Lop
    README](http://lcamtuf.coredump.cx/afl/README.txt)

3. [PNG/MNG formats forum at
    Sourceforge](https://sourceforge.net/p/png-mng/mailman/message/34626800/)
