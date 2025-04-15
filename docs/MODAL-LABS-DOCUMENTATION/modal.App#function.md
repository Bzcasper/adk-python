---
title: "Modal.App"
url: "https://modal.com/docs/reference/modal.App#function"
date: "2025-04-15 01:06:34"
word_count: 1463
---

# Modal.App

**Source:** [https://modal.com/docs/reference/modal.App#function](https://modal.com/docs/reference/modal.App#function)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1463

## Table of Contents

- [modal.App](#modalapp)
  - [is_interactive](#isinteractive)
  - [app_id](#appid)
  - [description](#description)
  - [lookup](#lookup)
  - [registered_functions](#registeredfunctions)
  - [registered_classes](#registeredclasses)
  - [registered_entrypoints](#registeredentrypoints)
  - [indexed_objects](#indexedobjects)
  - [local_entrypoint](#localentrypoint)
  - [function](#function)
  - [cls](#cls)
  - [include](#include)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.App <a id="modalapp"></a>
```
class App(object)
```
 A Modal App is a group of functions and classes that are deployed together.
The app serves at least three purposes: * A unit of deployment for functions and classes. * Syncing of identities of (primarily) functions and classes across processes (your local Python interpreter and every Modal container active in your application). * Manage log collection for everything that happens inside your code. * *Registering functions with an app**
The most common way to explicitly register an Object with an app is through the `@app.function()` decorator. It both registers the annotated function itself and other passed objects, like schedules and secrets, with the app:
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
 In this example, the secret and schedule are registered with the app.
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
 Construct a new app, optionally with default image, mounts, secrets, or volumes.
```
image = modal.Image.debian_slim().pip_install(...)
secret = modal.Secret.from_name("my-secret")
volume = modal.Volume.from_name("my-data")
app = modal.App(image=image, secrets=[secret], volumes={"/mnt/data": volume})
```
 ## name
```
@property
def name(self) -> Optional[str]:
```
 The user-provided name of the App.
## is_interactive <a id="isinteractive"></a>
```
@property
def is_interactive(self) -> bool:
```
 Whether the current app for the app is running in interactive mode.
## app_id <a id="appid"></a>
```
@property
def app_id(self) -> Optional[str]:
```
 Return the app_id of a running or stopped app.
## description <a id="description"></a>
```
@property
def description(self) -> Optional[str]:
```
 The Apps `name`, if available, or a fallback descriptive identifier.
## lookup <a id="lookup"></a>
```
@staticmethod
@renamed_parameter((2024, 12, 18), "label", "name")
def lookup(
  name: str,
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  create_if_missing: bool = False,
) -> "_App":
```
 Look up an App with a given name, creating a new App if necessary.
Note that Apps created through this method will be in a deployed state, but they will not have any associated Functions or Classes. This method is mainly useful for creating an App to associate with a Sandbox:
```
app = modal.App.lookup("my-app", create_if_missing=True)
modal.Sandbox.create("echo", "hi", app=app)
```
 ## set_description
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
0 ## image
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
1 ## run
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
2 Context manager that runs an app on Modal.
Use this as the main entry point for your Modal application. All calls to Modal functions should be made within the scope of this context manager, and they will correspond to the current app.
* *Example**
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
3 To enable output printing, use `modal.enable_output()`:
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
4 Note that you cannot invoke this in global scope of a file where you have Modal functions or Classes, since that would run the block when the function or class is imported in your containers as well. If you want to run it as your entrypoint, consider wrapping it:
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
5 You can then run your script with:
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
6 Note that this method used to return a separate App object. This is no longer useful since you can use the app itself for access to all objects. For backwards compatibility reasons, it returns the same app.
## registered_functions <a id="registeredfunctions"></a>
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
7 All modal.Function objects registered on the app.
## registered_classes <a id="registeredclasses"></a>
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
8 All modal.Cls objects registered on the app.
## registered_entrypoints <a id="registeredentrypoints"></a>
```
import modal
app = modal.App()
@app.function(
  secrets=[modal.Secret.from_name("some_secret")],
  schedule=modal.Period(days=1),
)
def foo():
  pass
```
9 All local CLI entrypoints registered on the app.
## indexed_objects <a id="indexedobjects"></a>
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
0 ## registered_web_endpoints
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
1 Names of web endpoint (ie. webhook) functions registered on the app.
## local_entrypoint <a id="localentrypoint"></a>
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
2 Decorate a function to be used as a CLI entrypoint for a Modal App.
These functions can be used to define code that runs locally to set up the app, and act as an entrypoint to start Modal functions from. Note that regular Modal functions can also be used as CLI entrypoints, but unlike `local_entrypoint`, those functions are executed remotely directly.
* *Example**
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
3 You can call the function using `modal run` directly from the CLI:
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
4 Note that an explicit `app.run()` (https://modal.com/docs/reference/modal.App# run) is not needed, as an app (https://modal.com/docs/guide/apps) is automatically created for you.
* *Multiple Entrypoints**
If you have multiple `local_entrypoint` functions, you can qualify the name of your app and function:
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
5 * *Parsing Arguments**
If your entrypoint function take arguments with primitive types, `modal run` automatically parses them as CLI options. For example, the following function can be called with `modal run app_module.py --foo 1 --bar "hello"`:
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
6 Currently, `str`, `int`, `float`, `bool`, and `datetime.datetime` are supported. Use `modal run app_module.py --help` for more information on usage.
## function <a id="function"></a>
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
7 Decorator to register a new Modal Function (https://modal.com/docs/reference/modal.Function) with this App.
## cls <a id="cls"></a>
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
8 Decorator to register a new Modal Cls (https://modal.com/docs/reference/modal.Cls) with this App.
## include <a id="include"></a>
```
def __init__(
  self,
  name: Optional[str] = None,
  *,
  image: Optional[_Image] = None, # default image for all functions (default is `modal.Image.debian_slim()`)
  mounts: Sequence[_Mount] = [], # default mounts for all functions
  secrets: Sequence[_Secret] = [], # default secrets for all functions
  volumes: dict[Union[str, PurePosixPath], _Volume] = {}, # default volumes for all functions
  include_source: Optional[bool] = None,
) -> None:
```
9 Include another Apps objects in this one.
Useful for splitting up Modal Apps across different self-contained files.
```
image = modal.Image.debian_slim().pip_install(...)
secret = modal.Secret.from_name("my-secret")
volume = modal.Volume.from_name("my-data")
app = modal.App(image=image, secrets=[secret], volumes={"/mnt/data": volume})
```
0 modal.App (https://modal.com/docs/reference/modal.App# modalapp)name (https://modal.com/docs/reference/modal.App# name)is_interactive (https://modal.com/docs/reference/modal.App# is_interactive)app_id (https://modal.com/docs/reference/modal.App# app_id)description (https://modal.com/docs/reference/modal.App# description)lookup (https://modal.com/docs/reference/modal.App# lookup)set_description (https://modal.com/docs/reference/modal.App# set_description)image (https://modal.com/docs/reference/modal.App# image)run (https://modal.com/docs/reference/modal.App# run)registered_functions (https://modal.com/docs/reference/modal.App# registered_functions)registered_classes (https://modal.com/docs/reference/modal.App# registered_classes)registered_entrypoints (https://modal.com/docs/reference/modal.App# registered_entrypoints)indexed_objects (https://modal.com/docs/reference/modal.App# indexed_objects)registered_web_endpoints (https://modal.com/docs/reference/modal.App# registered_web_endpoints)local_entrypoint (https://modal.com/docs/reference/modal.App# local_entrypoint)function (https://modal.com/docs/reference/modal.App# function)cls (https://modal.com/docs/reference/modal.App# cls)include (https://modal.com/docs/reference/modal.App# include)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)