---
title: "Modal.Networkfilesystem"
url: "https://modal.com/docs/reference/modal.NetworkFileSystem"
date: "2025-04-15 01:06:34"
word_count: 1165
---

# Modal.Networkfilesystem

**Source:** [https://modal.com/docs/reference/modal.NetworkFileSystem](https://modal.com/docs/reference/modal.NetworkFileSystem)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1165

## Table of Contents

- [modal.NetworkFileSystem](#modalnetworkfilesystem)
  - [from_name](#fromname)
  - [read_file](#readfile)
  - [iterdir](#iterdir)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.NetworkFileSystem <a id="modalnetworkfilesystem"></a>
```
class NetworkFileSystem(modal.object.Object)
```
 A shared, writable file system accessible by one or more Modal functions.
By attaching this file system as a mount to one or more functions, they can share and persist data with each other.
* *Usage**
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
 Also see the CLI methods for accessing network file systems:
```
modal nfs --help
```
 A `NetworkFileSystem` can also be useful for some local scripting scenarios, e.g.:
```
nfs = modal.NetworkFileSystem.from_name("my-network-file-system")
for chunk in nfs.read_file("my_db_dump.csv"):
  ...
```
```
def __init__(self, *args, **kwargs):
```
 ## hydrate
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
 Synchronize the local object with its identity on the Modal server.
It is rarely necessary to call this method explicitly, as most operations will lazily hydrate when needed. The main use case is when you need to access object metadata, such as its ID.
_Added in v0.72.39_ : This method replaces the deprecated `.resolve()` method.
## from_name <a id="fromname"></a>
```
@staticmethod
@renamed_parameter((2024, 12, 18), "label", "name")
def from_name(
  name: str,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  environment_name: Optional[str] = None,
  create_if_missing: bool = False,
) -> "_NetworkFileSystem":
```
 Reference a NetworkFileSystem by its name, creating if necessary.
In contrast to `modal.NetworkFileSystem.lookup`, this is a lazy method that defers hydrating the local object with metadata from Modal servers until the first time it is actually used.
```
nfs = NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
@app.function(network_file_systems={"/data": nfs})
def f():
  pass
```
 ## ephemeral
```
@classmethod
@contextmanager
def ephemeral(
  cls: type["_NetworkFileSystem"],
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  _heartbeat_sleep: float = EPHEMERAL_OBJECT_HEARTBEAT_SLEEP,
) -> Iterator["_NetworkFileSystem"]:
```
 Creates a new ephemeral network filesystem within a context manager:
Usage:
```
with modal.NetworkFileSystem.ephemeral() as nfs:
  assert nfs.listdir("/") == []
```
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
0 ## lookup
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
1 Lookup a named NetworkFileSystem.
DEPRECATED: This method is deprecated in favor of `modal.NetworkFileSystem.from_name`.
In contrast to `modal.NetworkFileSystem.from_name`, this is an eager method that will hydrate the local object with metadata from Modal servers.
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
2 ## delete
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
3 ## write_file
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
4 Write from a file object to a path on the network file system, atomically.
Will create any needed parent directories automatically.
If remote_path ends with `/` its assumed to be a directory and the file will be uploaded with its current name to that directory.
## read_file <a id="readfile"></a>
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
5 Read a file from the network file system
## iterdir <a id="iterdir"></a>
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
6 Iterate over all files in a directory in the network file system. * Passing a directory path lists all files in the directory (names are relative to the directory) * Passing a file path returns a list containing only that files listing description * Passing a glob path (including at least one * or ** sequence) returns all files matching that glob path (using absolute paths) ## add_local_file
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
7 ## add_local_dir
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
8 ## listdir
```
import modal
nfs = modal.NetworkFileSystem.from_name("my-nfs", create_if_missing=True)
app = modal.App()
@app.function(network_file_systems={"/root/foo": nfs})
def f():
  pass
@app.function(network_file_systems={"/root/goo": nfs})
def g():
  pass
```
9 List all files in a directory in the network file system. * Passing a directory path lists all files in the directory (names are relative to the directory) * Passing a file path returns a list containing only that files listing description * Passing a glob path (including at least one * or ** sequence) returns all files matching that glob path (using absolute paths) ## remove_file
```
modal nfs --help
```
0 Remove a file in a network file system.
modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem# modalnetworkfilesystem)hydrate (https://modal.com/docs/reference/modal.NetworkFileSystem# hydrate)from_name (https://modal.com/docs/reference/modal.NetworkFileSystem# from_name)ephemeral (https://modal.com/docs/reference/modal.NetworkFileSystem# ephemeral)lookup (https://modal.com/docs/reference/modal.NetworkFileSystem# lookup)delete (https://modal.com/docs/reference/modal.NetworkFileSystem# delete)write_file (https://modal.com/docs/reference/modal.NetworkFileSystem# write_file)read_file (https://modal.com/docs/reference/modal.NetworkFileSystem# read_file)iterdir (https://modal.com/docs/reference/modal.NetworkFileSystem# iterdir)add_local_file (https://modal.com/docs/reference/modal.NetworkFileSystem# add_local_file)add_local_dir (https://modal.com/docs/reference/modal.NetworkFileSystem# add_local_dir)listdir (https://modal.com/docs/reference/modal.NetworkFileSystem# listdir)remove_file (https://modal.com/docs/reference/modal.NetworkFileSystem# remove_file)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)