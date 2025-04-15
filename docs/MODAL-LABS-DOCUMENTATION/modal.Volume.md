---
title: "Modal.Volume"
url: "https://modal.com/docs/reference/modal.Volume"
date: "2025-04-15 01:06:34"
word_count: 1441
---

# Modal.Volume

**Source:** [https://modal.com/docs/reference/modal.Volume](https://modal.com/docs/reference/modal.Volume)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1441

## Table of Contents

- [modal.Volume](#modalvolume)
  - [from_name](#fromname)
- [Volume refers to the same object, even across instances of `app`.](#volume-refers-to-the-same-object-even-across-instances-of-app)
  - [reload](#reload)
  - [iterdir](#iterdir)
  - [listdir](#listdir)
  - [read_file](#readfile)
  - [copy_files](#copyfiles)
  - [batch_upload](#batchupload)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Volume <a id="modalvolume"></a>
```
class Volume(modal.object.Object)
```
 A writeable volume that can be used to share files between one or more Modal functions.
The contents of a volume is exposed as a filesystem. You can use it to share data between different functions, or to persist durable state across several instances of the same function.
Unlike a networked filesystem, you need to explicitly reload the volume to see changes made since it was mounted. Similarly, you need to explicitly commit any changes you make to the volume for the changes to become visible outside the current container.
Concurrent modification is supported, but concurrent modifications of the same files should be avoided! Last write wins in case of concurrent modification of the same file - any data the last writer didnt have when committing changes will be lost!
As a result, volumes are typically not a good fit for use cases where you need to make concurrent modifications to the same file (nor is distributed file locking supported).
Volumes can only be reloaded if there are no open files for the volume - attempting to reload with open files will result in an error.
* *Usage**
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
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
  version: "typing.Optional[modal_proto.api_pb2.VolumeFsVersion.ValueType]" = None,
) -> "_Volume":
```
 Reference a Volume by name, creating if necessary.
In contrast to `modal.Volume.lookup`, this is a lazy method that defers hydrating the local object with metadata from Modal servers until the first time is is actually used.
```
vol = modal.Volume.from_name("my-volume", create_if_missing=True)
app = modal.App()
# Volume refers to the same object, even across instances of `app`. <a id="volume-refers-to-the-same-object-even-across-instances-of-app"></a>
@app.function(volumes={"/data": vol})
def f():
  pass
```
 ## ephemeral
```
@classmethod
@contextmanager
def ephemeral(
  cls: type["_Volume"],
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  version: "typing.Optional[modal_proto.api_pb2.VolumeFsVersion.ValueType]" = None,
  _heartbeat_sleep: float = EPHEMERAL_OBJECT_HEARTBEAT_SLEEP,
) -> AsyncGenerator["_Volume", None]:
```
 Creates a new ephemeral volume within a context manager:
Usage:
```
import modal
with modal.Volume.ephemeral() as vol:
  assert vol.listdir("/") == []
```
```
async with modal.Volume.ephemeral() as vol:
  assert await vol.listdir("/") == []
```
 ## lookup
```
@staticmethod
@renamed_parameter((2024, 12, 18), "label", "name")
def lookup(
  name: str,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  create_if_missing: bool = False,
  version: "typing.Optional[modal_proto.api_pb2.VolumeFsVersion.ValueType]" = None,
) -> "_Volume":
```
 Lookup a named Volume.
DEPRECATED: This method is deprecated in favor of `modal.Volume.from_name`.
In contrast to `modal.Volume.from_name`, this is an eager method that will hydrate the local object with metadata from Modal servers.
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
0 ## commit
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
1 Commit changes to the volume.
If successful, the changes made are now persisted in durable storage and available to other containers accessing the volume.
## reload <a id="reload"></a>
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
2 Make latest committed state of volume available in the running container.
Any uncommitted changes to the volume, such as new or modified files, may implicitly be committed when reloading.
Reloading will fail if there are open files for the volume.
## iterdir <a id="iterdir"></a>
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
3 Iterate over all files in a directory in the volume.
Passing a directory path lists all files in the directory. For a file path, return only that files description. If `recursive` is set to True, list all files and folders under the path recursively.
## listdir <a id="listdir"></a>
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
4 List all files under a path prefix in the modal.Volume.
Passing a directory path lists all files in the directory. For a file path, return only that files description. If `recursive` is set to True, list all files and folders under the path recursively.
## read_file <a id="readfile"></a>
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
5 Read a file from the modal.Volume.
* *Example:**
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
6 ## remove_file
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
7 Remove a file or directory from a volume.
## copy_files <a id="copyfiles"></a>
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
8 files within the volume from src_paths to dst_path. The semantics of the operation follow those of the UNIX cp command.
The `src_paths` parameter is a list. If you want to a single file, you should pass a list with a single element.
`src_paths` and `dst_path` should refer to the desired location _inside_ the volume. You do not need to prepend the volume mount path.
* *Usage**
```
import modal
app = modal.App()
volume = modal.Volume.from_name("my-persisted-volume", create_if_missing=True)
@app.function(volumes={"/root/foo": volume})
def f():
  with open("/root/foo/bar.txt", "w") as f:
    f.write("hello")
  volume.commit() # Persist changes
@app.function(volumes={"/root/foo": volume})
def g():
  volume.reload() # Fetch latest changes
  with open("/root/foo/bar.txt", "r") as f:
    print(f.read())
```
9 Note that if the volume is already mounted on the Modal function, you should use normal filesystem operations like `os.rename()` and then `commit()` the volume. The `copy_files()` method is useful when you dont have the volume mounted as a filesystem, e.g. when running a script on your local computer.
## batch_upload <a id="batchupload"></a>
```
def __init__(self, *args, **kwargs):
```
0 Initiate a batched upload to a volume.
To allow overwriting existing files, set `force` to `True` (you cannot overwrite existing directories with uploaded files regardless).
* *Example:**
```
def __init__(self, *args, **kwargs):
```
1 ## delete
```
def __init__(self, *args, **kwargs):
```
2 ## rename
```
def __init__(self, *args, **kwargs):
```
3 modal.Volume (https://modal.com/docs/reference/modal.Volume# modalvolume)hydrate (https://modal.com/docs/reference/modal.Volume# hydrate)from_name (https://modal.com/docs/reference/modal.Volume# from_name)ephemeral (https://modal.com/docs/reference/modal.Volume# ephemeral)lookup (https://modal.com/docs/reference/modal.Volume# lookup)commit (https://modal.com/docs/reference/modal.Volume# commit)reload (https://modal.com/docs/reference/modal.Volume# reload)iterdir (https://modal.com/docs/reference/modal.Volume# iterdir)listdir (https://modal.com/docs/reference/modal.Volume# listdir)read_file (https://modal.com/docs/reference/modal.Volume# read_file)remove_file (https://modal.com/docs/reference/modal.Volume# remove_file)copy_files (https://modal.com/docs/reference/modal.Volume# copy_files)batch_upload (https://modal.com/docs/reference/modal.Volume# batch_upload)delete (https://modal.com/docs/reference/modal.Volume# delete)rename (https://modal.com/docs/reference/modal.Volume# rename)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)