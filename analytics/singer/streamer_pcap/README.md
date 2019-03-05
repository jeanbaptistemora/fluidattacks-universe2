# Streamer PCAP

Reads a [Packet Capture file (PCAP)](https://en.wikipedia.org/wiki/Pcap)
created with a software like [TCP dump](https://www.tcpdump.org/)
and persist it to stdout as a JSON formatted stream.

# How to install
Download a fresh copy of the source code and install it with pip:

```bash
$ cd streamer_pcap
$ python3 -m pip install .
```

Installation requires python 3.6 or later.

# How to use
Record some network traffic and dump it to a PCAP file.

```bash
$ ./record.sh
```

This will create 1MB PCAP files in `/var/tmp/pcap/`.

Then run this script against the dumped files:

```bash
$ ./process.sh
```

And use any Singer Target to push this information locally to a CSV file
or remotely to your data warehouse.

# Sponsor

[Fluid attacks](https://fluidattacks.com/)
