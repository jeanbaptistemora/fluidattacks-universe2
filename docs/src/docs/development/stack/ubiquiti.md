---
id: ubiquiti
title: Ubiquiti
sidebar_label: Ubiquiti
slug: /development/stack/ubiquiti
---

## Rationale

[Ubiquiti][UBIQUITI]
EdgeRouter 8 is the router we mainly use
to create VPN tunnels with some clients.

## Usage

In order to configure the router or look for any configurations
You have to ask for the credentials at help@fluidattacks.com.

1. When you have the credentials you can access the router via `ssh`
   `ssh technology@$router-ip` where `$router-ip` will be given
   in the ticket created via email.
1. After you access the router via ssh you will be asked for a
   password, which will be given in the ticket.
1. Once you loged in the router, you can go to configuration
   mode by entering `configure`.

### Setting up VPN's

To be able to set up a VPN you have to be in configuration mode.

We have documented the process to set up a
VPN tunnel:

1. Set up the authentication mode. Example:
   `set vpn ipsec site-to-site peer $client-peer authentication mode pre-shared-secret`
   where `$client-peer` is the peer given by the client.
1. Generate pre-shared-key secret, we generate this key using
   `openssl rand -base64 24`.
1. Set up the `pre-shared-key` secret. Example:

   ```bash
    set vpn ipsec site-to-site peer $client-peer authentication pre-shared-secret $secret
   ```

   where `$secret` is the value generated in the previous step.
1. Set up a description/name for the VPN tunnel. Example:
   `set vpn ipsec site-to-site peer $client-peer description $vpn-name`
   where `$vpn-name` can be anything to identify the tunnel.
1. Set up the local address for the tunnel. Example:
   `set vpn ipsec site-to-site peer $client-peer local-address $local-ip`
   where `$local-ip` can be Any `0.0.0.0` or a local ip from the router,
   in this case we already have one IP ready to use, you can
   look it up by running this command
   `show vpn l2tp remote-access outside-address`.
1. Create a new `ike-group` which is determined for the phase 1. Example:
   `set vpn ipsec ike-group $group-name` where `$group-name` is standarized
   to be named starting with an `F` followed by a three digit number `001`
   Example: `F001`.
   To set up this group configuration you have to enter these commands
   changing the values according to your needs:

   ```bash
    set vpn ipsec ike-group FOO1 proposal 1 dh-group 2
    set vpn ipsec ike-group FOO1 proposal 1 encryption aes128
    set vpn ipsec ike-group FOO1 proposal 1 hash sha1
    set vpn ipsec ike-group FOO1 dead-peer-detection action restart
    set vpn ipsec ike-group FOO1 dead-peer-detection interval 15
    set vpn ipsec ike-group FOO1 dead-peer-detection timeout 30
   ```

1. Attach the `ike-group` to the VPN. Example:
   `set vpn ipsec site-to-site peer $client-peer ike-group $ike-group-name`.
1. Create a new `esp-group` which is determined for the phase 2. Example:
   `set vpn ipsec esp-group $group-name` `$group-name` is standarized
   to be named starting with an `F` followed by a three digit number `001`.
   This name is attached to the `ike-group`, so it must be the same name.
   Example: `F001`
   To set up this group configuration you have to enter these commands
   changing the values according to your needs:

   ```bash
    set vpn ipsec esp-group FOO1 lifetime 3600
    set vpn ipsec esp-group FOO1 pfs enable
    set vpn ipsec esp-group FOO1 proposal 1 encryption aes128
    set vpn ipsec esp-group FOO1 proposal 1 hash sha1
   ```

1. Attach the `esp-group` to the VPN. This attachment must be done for
   each tunnel. Example:
   `set vpn ipsec site-to-site peer $client-peer tunnel 1 esp-group $esp-group`.
1. Set up each tunnel connection. Example:
   `set vpn ipsec site-to-site peer $client-peer tunnel 1 local prefix $local-prefix`
   where `$local-prefix` is an ip between a range declared. You can look
   it up using this command `show vpn l2tp remote-access client-ip-pool` and
   taking an available ip, this ip can be shared between tunnels.
1. Set up the destination ip. Example:
   `set vpn ipsec site-to-site peer $client-peer 1 remote prefix $client-remote`
   where `$client-remote` is the remote IP which the tunnel will connect.
1. After you configure the VPN tunnel you have to commit the changes `commit`
   and save it `save`.

### Restarting VPN's

In order to restart a VPN run this command in configuration mode
`run clear vpn ipsec-peer $client-peer` where `$client-peer` is the
peer configured to that VPN, you can also specify a tunnel by adding `tunnel 1`
at the end of the command.

### Check VPN status

You can check the VPN status by running this command in configuration mode
`sudo ipsec status` This will prompt any configured tunnels, where any tunnel
with the word `INSTALLED` is a configured tunnel with status `up`, and any
`ROUTED` tunnel is a configured tunnel but with status `down`.

### Restart router

You can restart the router by running this command out of configuration mode
`reboot now`.

### Recommendations

The router has a Graphic user interface, which you can access by asking
for the permissions at help@fluidattacks.com.

This user interface can be used to view any configuration on the router,
but we do not encourage to make any changes here. By changing, for example,
any VPN tunnel configuration and commiting the changes, the router will reset
to default values the phase 1 and phase 2 proposals, so be careful here.

[UBIQUITI]: https://www.ui.com/
