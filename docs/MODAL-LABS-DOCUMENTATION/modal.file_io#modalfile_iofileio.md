---
title: "Modal.File Io"
url: "https://modal.com/docs/reference/modal.file_io#modalfile_iofileio"
date: "2025-04-15 01:06:34"
word_count: 1101
---

# Modal.File Io

**Source:** [https://modal.com/docs/reference/modal.file_io#modalfile_iofileio](https://modal.com/docs/reference/modal.file_io#modalfile_iofileio)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1101

## Table of Contents

- [modal.file_io](#modalfileio)
  - [modal.file_io.FileIO](#modalfileiofileio)
    - [read](#read)
    - [readline](#readline)
    - [readlines](#readlines)
    - [write](#write)
    - [flush](#flush)
    - [seek](#seek)
    - [ls](#ls)
    - [mkdir](#mkdir)
    - [rm](#rm)
    - [watch](#watch)
  - [modal.file_io.FileWatchEvent](#modalfileiofilewatchevent)
  - [modal.file_io.replace_bytes](#modalfileioreplacebytes)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.file_io <a id="modalfileio"></a>
## modal.file_io.FileIO <a id="modalfileiofileio"></a>
```
class FileIO(typing.Generic)
```
 FileIO handle, used in the Sandbox filesystem API.
The API is designed to mimic Pythons io.FileIO.
* *Usage**
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
```
def __init__(self, client: _Client, task_id: str) -> None:
```
 ### create
```
@classmethod
def create(
  cls, path: str, mode: Union["_typeshed.OpenTextMode", "_typeshed.OpenBinaryMode"], client: _Client, task_id: str
) -> "_FileIO":
```
 Create a new FileIO handle.
### read <a id="read"></a>
```
def read(self, n: Optional[int] = None) -> T:
```
 Read n bytes from the current position, or the entire remaining file if n is None.
### readline <a id="readline"></a>
```
def readline(self) -> T:
```
 Read a single line from the current position.
### readlines <a id="readlines"></a>
```
def readlines(self) -> Sequence[T]:
```
 Read all lines from the current position.
### write <a id="write"></a>
```
def write(self, data: Union[bytes, str]) -> None:
```
 Write data to the current position.
Writes may not appear until the entire buffer is flushed, which can be done manually with `flush()` or automatically when the file is closed.
### flush <a id="flush"></a>
```
def flush(self) -> None:
```
 Flush the buffer to disk.
### seek <a id="seek"></a>
```
def seek(self, offset: int, whence: int = 0) -> None:
```
 Move to a new position in the file.
`whence` defaults to 0 (absolute file positioning); other values are 1 (relative to the current position) and 2 (relative to the files end).
### ls <a id="ls"></a>
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
0 List the contents of the provided directory.
### mkdir <a id="mkdir"></a>
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
1 Create a new directory.
### rm <a id="rm"></a>
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
2 Remove a file or directory in the Sandbox.
### watch <a id="watch"></a>
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
3 ### close
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
4 Flush the buffer and close the file.
## modal.file_io.FileWatchEvent <a id="modalfileiofilewatchevent"></a>
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
5 FileWatchEvent(paths: list[str], type: modal.file_io.FileWatchEventType)
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
6 ## modal.file_io.FileWatchEventType
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
7 An enumeration.
The possible values are: * `Unknown` * `Access` * `Create` * `Modify` * `Remove` ## modal.file_io.delete_bytes
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
8 Delete a range of bytes from the file.
`start` and `end` are byte offsets. `start` is inclusive, `end` is exclusive. If either is None, the start or end of the file is used, respectively.
## modal.file_io.replace_bytes <a id="modalfileioreplacebytes"></a>
```
import modal
app = modal.App.lookup("my-app", create_if_missing=True)
sb = modal.Sandbox.create(app=app)
f = sb.open("/tmp/foo.txt", "w")
f.write("hello")
f.close()
```
9 Replace a range of bytes in the file with new data. The length of the data does not have to be the same as the length of the range being replaced.
`start` and `end` are byte offsets. `start` is inclusive, `end` is exclusive. If either is None, the start or end of the file is used, respectively.
modal.file_io (https://modal.com/docs/reference/modal.file_io# modalfile_io)modal.file_io.FileIO (https://modal.com/docs/reference/modal.file_io# modalfile_iofileio)create (https://modal.com/docs/reference/modal.file_io# create)read (https://modal.com/docs/reference/modal.file_io# read)readline (https://modal.com/docs/reference/modal.file_io# readline)readlines (https://modal.com/docs/reference/modal.file_io# readlines)write (https://modal.com/docs/reference/modal.file_io# write)flush (https://modal.com/docs/reference/modal.file_io# flush)seek (https://modal.com/docs/reference/modal.file_io# seek)ls (https://modal.com/docs/reference/modal.file_io# ls)mkdir (https://modal.com/docs/reference/modal.file_io# mkdir)rm (https://modal.com/docs/reference/modal.file_io# rm)watch (https://modal.com/docs/reference/modal.file_io# watch)close (https://modal.com/docs/reference/modal.file_io# close)modal.file_io.FileWatchEvent (https://modal.com/docs/reference/modal.file_io# modalfile_iofilewatchevent)modal.file_io.FileWatchEventType (https://modal.com/docs/reference/modal.file_io# modalfile_iofilewatcheventtype)modal.file_io.delete_bytes (https://modal.com/docs/reference/modal.file_io# modalfile_iodelete_bytes)modal.file_io.replace_bytes (https://modal.com/docs/reference/modal.file_io# modalfile_ioreplace_bytes)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)