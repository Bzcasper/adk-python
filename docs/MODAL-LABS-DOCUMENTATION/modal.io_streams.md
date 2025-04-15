---
title: "Modal.Io Streams"
url: "https://modal.com/docs/reference/modal.io_streams"
date: "2025-04-15 01:06:34"
word_count: 923
---

# Modal.Io Streams

**Source:** [https://modal.com/docs/reference/modal.io_streams](https://modal.com/docs/reference/modal.io_streams)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 923

## Table of Contents

- [modal.io_streams](#modaliostreams)
  - [modal.io_streams.StreamReader](#modaliostreamsstreamreader)
    - [read](#read)
    - [write](#write)
    - [drain](#drain)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.io_streams <a id="modaliostreams"></a>
## modal.io_streams.StreamReader <a id="modaliostreamsstreamreader"></a>
```
class StreamReader(typing.Generic)
```
 Retrieve logs from a stream (`stdout` or `stderr`).
As an asynchronous iterable, the object supports the `for` and `async for` statements. Just loop over the object to read in chunks.
* *Usage**
```
from modal import Sandbox
sandbox = Sandbox.create(
  "bash",
  "-c",
  "for i in $(seq 1 10); do echo foo; sleep 0.1; done",
  app=running_app,
)
for message in sandbox.stdout:
  print(f"Message: {message}")
```
 ### file_descriptor
```
@property
def file_descriptor(self) -> int:
```
 Possible values are `1` for stdout and `2` for stderr.
### read <a id="read"></a>
```
def read(self) -> T:
```
 Fetch the entire contents of the stream until EOF.
* *Usage**
```
from modal import Sandbox
sandbox = Sandbox.create("echo", "hello", app=running_app)
sandbox.wait()
print(sandbox.stdout.read())
```
 ## modal.io_streams.StreamWriter
```
class StreamWriter(object)
```
 Provides an interface to buffer and write logs to a sandbox or container process stream (`stdin`).
### write <a id="write"></a>
```
def write(self, data: Union[bytes, bytearray, memoryview, str]) -> None:
```
 Write data to the stream but does not send it immediately.
This is non-blocking and queues the data to an internal buffer. Must be used along with the `drain()` method, which flushes the buffer.
* *Usage**
```
from modal import Sandbox
sandbox = Sandbox.create(
  "bash",
  "-c",
  "while read line; do echo $line; done",
  app=running_app,
)
sandbox.stdin.write(b"foo\n")
sandbox.stdin.write(b"bar\n")
sandbox.stdin.write_eof()
sandbox.stdin.drain()
sandbox.wait()
```
 ### write_eof
```
def write_eof(self) -> None:
```
 Close the write end of the stream after the buffered data is drained.
If the process was blocked on input, it will become unblocked after `write_eof()`. This method needs to be used along with the `drain()` method, which flushes the EOF to the process.
### drain <a id="drain"></a>
```
def drain(self) -> None:
```
 Flush the write buffer and send data to the running process.
This is a flow control method that blocks until data is sent. It returns when it is appropriate to continue writing data to the stream.
* *Usage**
```
from modal import Sandbox
sandbox = Sandbox.create(
  "bash",
  "-c",
  "for i in $(seq 1 10); do echo foo; sleep 0.1; done",
  app=running_app,
)
for message in sandbox.stdout:
  print(f"Message: {message}")
```
0 Async usage:
```
from modal import Sandbox
sandbox = Sandbox.create(
  "bash",
  "-c",
  "for i in $(seq 1 10); do echo foo; sleep 0.1; done",
  app=running_app,
)
for message in sandbox.stdout:
  print(f"Message: {message}")
```
1 modal.io_streams (https://modal.com/docs/reference/modal.io_streams# modalio_streams)modal.io_streams.StreamReader (https://modal.com/docs/reference/modal.io_streams# modalio_streamsstreamreader)file_descriptor (https://modal.com/docs/reference/modal.io_streams# file_descriptor)read (https://modal.com/docs/reference/modal.io_streams# read)modal.io_streams.StreamWriter (https://modal.com/docs/reference/modal.io_streams# modalio_streamsstreamwriter)write (https://modal.com/docs/reference/modal.io_streams# write)write_eof (https://modal.com/docs/reference/modal.io_streams# write_eof)drain (https://modal.com/docs/reference/modal.io_streams# drain)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)