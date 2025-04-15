---
title: "Modal.Forward"
url: "https://modal.com/docs/reference/modal.forward"
date: "2025-04-15 01:06:34"
word_count: 815
---

# Modal.Forward

**Source:** [https://modal.com/docs/reference/modal.forward](https://modal.com/docs/reference/modal.forward)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 815

## Table of Contents

- [modal.forward](#modalforward)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.forward <a id="modalforward"></a>
```
@contextmanager
def forward(port: int, *, unencrypted: bool = False, client: Optional[_Client] = None) -> Iterator[Tunnel]:
```
 Expose a port publicly from inside a running Modal container, with TLS.
If `unencrypted` is set, this also exposes the TCP socket without encryption on a random port number. This can be used to SSH into a container (see example below). Note that it is on the public Internet, so make sure you are using a secure protocol over TCP.
* *Important:** This is an experimental API which may change in the future.
* *Usage:**
```
import modal
from flask import Flask
app = modal.App(image=modal.Image.debian_slim().pip_install("Flask"))
flask_app = Flask(__name__)
@flask_app.route("/")
def hello_world():
  return "Hello, World!"
@app.function()
def run_app():
  # Start a web server inside the container at port 8000. `modal.forward(8000)` lets us
  # expose that port to the world at a random HTTPS URL.
  with modal.forward(8000) as tunnel:
    print("Server listening at", tunnel.url)
    flask_app.run("0.0.0.0", 8000)
  # When the context manager exits, the port is no longer exposed.
```
 * *Raw TCP usage:**
```
import socket
import threading
import modal
def run_echo_server(port: int):
  """Run a TCP echo server listening on the given port."""
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(("0.0.0.0", port))
  sock.listen(1)
  while True:
    conn, addr = sock.accept()
    print("Connection from:", addr)
    # Start a new thread to handle the connection
    def handle(conn):
      with conn:
        while True:
          data = conn.recv(1024)
          if not data:
            break
          conn.sendall(data)
    threading.Thread(target=handle, args=(conn,)).start()
app = modal.App()
@app.function()
def tcp_tunnel():
  # This exposes port 8000 to public Internet traffic over TCP.
  with modal.forward(8000, unencrypted=True) as tunnel:
    # You can connect to this TCP socket from outside the container, for example, using `nc`:
    # nc <HOST> <PORT>
    print("TCP tunnel listening at:", tunnel.tcp_socket)
    run_echo_server(8000)
```
 * *SSH example:** This assumes you have a rsa keypair in `~/.ssh/id_rsa{.pub}`, this is a bare-bones example letting you SSH into a Modal container.
```
import subprocess
import time
import modal
app = modal.App()
image = (
  modal.Image.debian_slim()
  .apt_install("openssh-server")
  .run_commands("mkdir /run/sshd")
  .add_local_file("~/.ssh/id_rsa.pub", "/root/.ssh/authorized_keys", =True)
)
@app.function(image=image, timeout=3600)
def some_function():
  subprocess.Popen(["/usr/sbin/sshd", "-D", "-e"])
  with modal.forward(port=22, unencrypted=True) as tunnel:
    hostname, port = tunnel.tcp_socket
    connection_cmd = f'ssh -p {port} root@{hostname}'
    print(f"ssh into container using: {connection_cmd}")
    time.sleep(3600) # keep alive for 1 hour or until killed
```
 If you intend to use this more generally, a suggestion is to put the subprocess and port forwarding code in an `@enter` lifecycle method of an @app.cls, to only make a single ssh server and port for each container (and not one for each input to the function).
modal.forward (https://modal.com/docs/reference/modal.forward# modalforward)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)