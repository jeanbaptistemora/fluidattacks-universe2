# Tap JSON

Reads a [JSON](https://www.json.org/) formatted stream from stdin
and persist it as a [Singer](https://www.singer.io/) formatted stream to stdout.

# How to install
Download a fresh copy of the source code and install with pip:

```bash
$ cd tap-json/
$ python3 -m pip install .
```

Installation requires python 3.7 or later.

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
