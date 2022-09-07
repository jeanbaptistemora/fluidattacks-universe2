<!--
SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>

SPDX-License-Identifier: MPL-2.0
-->

# Tap JSON

Reads a [JSON](https://www.json.org/) formatted stream from stdin
and persist it as a [Singer](https://www.singer.io/) formatted stream to stdout.

# How to use

Just connect tap-json's stdin to the stdout of any JSON streamer:

```bash
$ streamer-anystreamer | tap-json
```

The output can be used to push data to any singer target:

```bash
$ streamer-anystreamer | tap-json | target-anytarget
```

# Sponsor

[Fluid attacks](https://fluidattacks.com/)
