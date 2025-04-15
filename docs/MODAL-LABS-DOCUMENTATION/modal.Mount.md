---
title: "Modal.Mount"
url: "https://modal.com/docs/reference/modal.Mount"
date: "2025-04-15 01:06:34"
word_count: 923
---

# Modal.Mount

**Source:** [https://modal.com/docs/reference/modal.Mount](https://modal.com/docs/reference/modal.Mount)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 923

## Table of Contents

- [modal.Mount](#modalmount)
  - [add_local_dir](#addlocaldir)
  - [from_local_dir](#fromlocaldir)
  - [from_local_file](#fromlocalfile)
- [Mount the DBT profile in user's home directory into container.](#mount-the-dbt-profile-in-users-home-directory-into-container)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Mount <a id="modalmount"></a>
```
class Mount(modal.object.Object)
```
 * *Deprecated** : Mounts should not be used explicitly anymore, use `Image.add_local_*` commands instead.
Create a mount for a local directory or file that can be attached to one or more Modal functions.
* *Usage**
```
import modal
import os
app = modal.App()
@app.function(mounts=[modal.Mount.from_local_dir("~/foo", remote_path="/root/foo")])
def f():
  # `/root/foo` has the contents of `~/foo`.
  print(os.listdir("/root/foo/"))
```
 Modal syncs the contents of the local directory every time the app runs, but uses the hash of the files contents to skip uploading files that have been uploaded before.
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
## add_local_dir <a id="addlocaldir"></a>
```
def add_local_dir(
  self,
  local_path: Union[str, Path],
  *,
  # Where the directory is placed within in the mount
  remote_path: Union[str, PurePosixPath, None] = None,
  # Predicate filter function for file selection, which should accept a filepath and return `True` for inclusion.
  # Defaults to including all files.
  condition: Optional[Callable[[str], bool]] = None,
  # add files from subdirectories as well
  recursive: bool = True,
) -> "_Mount":
```
 Add a local directory to the `Mount` object.
## from_local_dir <a id="fromlocaldir"></a>
```
@staticmethod
def from_local_dir(
  local_path: Union[str, Path],
  *,
  # Where the directory is placed within in the mount
  remote_path: Union[str, PurePosixPath, None] = None,
  # Predicate filter function for file selection, which should accept a filepath and return `True` for inclusion.
  # Defaults to including all files.
  condition: Optional[Callable[[str], bool]] = None,
  # add files from subdirectories as well
  recursive: bool = True,
) -> "_Mount":
```
 * *Deprecated:** Use image.add_local_dir() instead
Create a `Mount` from a local directory.
* *Usage**
```
assets = modal.Mount.from_local_dir(
  "~/assets",
  condition=lambda pth: not ".venv" in pth,
  remote_path="/assets",
)
```
 ## add_local_file
```
def add_local_file(
  self,
  local_path: Union[str, Path],
  remote_path: Union[str, PurePosixPath, None] = None,
) -> "_Mount":
```
 Add a local file to the `Mount` object.
## from_local_file <a id="fromlocalfile"></a>
```
@staticmethod
def from_local_file(local_path: Union[str, Path], remote_path: Union[str, PurePosixPath, None] = None) -> "_Mount":
```
 * *Deprecated** : Use image.add_local_file() instead
Create a `Mount` mounting a single local file.
* *Usage**
```
# Mount the DBT profile in user's home directory into container. <a id="mount-the-dbt-profile-in-users-home-directory-into-container"></a>
dbt_profiles = modal.Mount.from_local_file(
  local_path="~/profiles.yml",
  remote_path="/root/dbt_profile/profiles.yml",
)
```
 ## from_local_python_packages
```
import modal
import os
app = modal.App()
@app.function(mounts=[modal.Mount.from_local_dir("~/foo", remote_path="/root/foo")])
def f():
  # `/root/foo` has the contents of `~/foo`.
  print(os.listdir("/root/foo/"))
```
0 * *Deprecated** : Use image.add_local_python_source instead
Returns a `modal.Mount` that makes local modules listed in `module_names` available inside the container. This works by mounting the local path of each modules package to a directory inside the container thats on `PYTHONPATH`.
* *Usage**
```
import modal
import os
app = modal.App()
@app.function(mounts=[modal.Mount.from_local_dir("~/foo", remote_path="/root/foo")])
def f():
  # `/root/foo` has the contents of `~/foo`.
  print(os.listdir("/root/foo/"))
```
1 modal.Mount (https://modal.com/docs/reference/modal.Mount# modalmount)hydrate (https://modal.com/docs/reference/modal.Mount# hydrate)add_local_dir (https://modal.com/docs/reference/modal.Mount# add_local_dir)from_local_dir (https://modal.com/docs/reference/modal.Mount# from_local_dir)add_local_file (https://modal.com/docs/reference/modal.Mount# add_local_file)from_local_file (https://modal.com/docs/reference/modal.Mount# from_local_file)from_local_python_packages (https://modal.com/docs/reference/modal.Mount# from_local_python_packages)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)