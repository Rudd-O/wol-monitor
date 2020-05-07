# `wol-monitor`: the Wake-on-LAN monitor

This program sits in the background listening for UDP connections coming on
ports 40000 and 9.  When a packet comes in any one of these ports,
`wol-monitor` writes a single byte (the ASCII character `1`) to all clients
connected to the UNIX socket `/run/wol-monitor/wol-bus`.

You can use this program to make sure that your own programs get notified
when WOL packets are sent to your machine, without having to write a complex
network server yourself -- all your programs must do is wait for bytes on
the socket above (after connecting to the socket, of course), and then react
accordingly.

## Security

For security reasons, this program creates the socket as UNIX user `root`
and group `root`, with read-only permission for the group.  This prevents
unprivileged programs from connecting to the WOL bus socket.  If you want
to change this, you can specify the group you'd like to make the socket
as, passing the name of the group as the first argument to the program.

The RPM package edition of this program creates a group `wol` which your
program can be a member of, and permits other programs to connect to the
WOL bus socket as long as they are members of said group.  You can change
that by tweaking the `/etc/default/wol-monitor` environment file, and
restarting the `wol-monitor` service.
