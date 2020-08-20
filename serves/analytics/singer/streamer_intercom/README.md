# Streamer intercom

Reads the [Intercom API](https://developers.intercom.com/),
and persist it as a JSON formatted stream on stdout.

# How to install
Download a fresh copy of the source code and install with pip:

```bash
$ cd streamer-intercom/
$ python3 -m pip install .
```

Installation requires python 3.6 or later.

# How to use
Create a JSON authentication file and save it as `auth.json`:

```json
{
    "access_token": "your access token",
}
```

Now pass it as an argument to the streamer:

```bash
$ streamer-intercom --auth auth.json
```

Output can be dumped to a singer formatted stream with the help of tap-JSON.
And later to any singer target.

```bash
$ streamer-intercom --auth auth.json | tap-json | target-redshift
```

# Sponsor

[Fluid attacks](https://fluidattacks.com/)
