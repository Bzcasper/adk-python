---
title: "Modal.Cls"
url: "https://modal.com/docs/reference/modal.Cls"
date: "2025-04-15 01:06:34"
word_count: 911
---

# Modal.Cls

**Source:** [https://modal.com/docs/reference/modal.Cls](https://modal.com/docs/reference/modal.Cls)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 911

## Table of Contents

- [modal.Cls](#modalcls)
  - [from_name](#fromname)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Cls <a id="modalcls"></a>
```
class Cls(modal.object.Object)
```
 Cls adds method pooling and lifecycle hook (https://modal.com/docs/guide/lifecycle-functions) behavior to modal.Function (https://modal.com/docs/reference/modal.Function).
Generally, you will not construct a Cls directly. Instead, use the `@app.cls()` (https://modal.com/docs/reference/modal.App# cls) decorator on the App object.
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
@classmethod
@renamed_parameter((2024, 12, 18), "tag", "name")
def from_name(
  cls: type["_Cls"],
  app_name: str,
  name: str,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  environment_name: Optional[str] = None,
  workspace: Optional[str] = None, # Deprecated and unused
) -> "_Cls":
```
 Reference a Cls from a deployed App by its name.
In contrast to `modal.Cls.lookup`, this is a lazy method that defers hydrating the local object with metadata from Modal servers until the first time it is actually used.
```
Model = modal.Cls.from_name("other-app", "Model")
```
 ## with_options
```
@warn_on_renamed_autoscaler_settings
def with_options(
  self: "_Cls",
  cpu: Optional[Union[float, tuple[float, float]]] = None,
  memory: Optional[Union[int, tuple[int, int]]] = None,
  gpu: GPU_T = None,
  secrets: Collection[_Secret] = (),
  volumes: dict[Union[str, os.PathLike], _Volume] = {},
  retries: Optional[Union[int, Retries]] = None,
  max_containers: Optional[int] = None, # Limit on the number of containers that can be concurrently running.
  scaledown_window: Optional[int] = None, # Max amount of time a container can remain idle before scaling down.
  timeout: Optional[int] = None,
  allow_concurrent_inputs: Optional[int] = None,
  # The following parameters are deprecated
  concurrency_limit: Optional[int] = None, # Now called `max_containers`
  container_idle_timeout: Optional[int] = None, # Now called `scaledown_window`
) -> "_Cls":
```
 * *Beta:** Allows for the runtime modification of a modal.Clss configuration.
This is a beta feature and may be unstable.
* *Usage:**
```
Model = modal.Cls.from_name("my_app", "Model")
ModelUsingGPU = Model.with_options(gpu="A100")
ModelUsingGPU().generate.remote(42) # will run with an A100 GPU
```
 ## lookup
```
@staticmethod
@renamed_parameter((2024, 12, 18), "tag", "name")
def lookup(
  app_name: str,
  name: str,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  workspace: Optional[str] = None, # Deprecated and unused
) -> "_Cls":
```
 Lookup a Cls from a deployed App by its name.
DEPRECATED: This method is deprecated in favor of `modal.Cls.from_name`.
In contrast to `modal.Cls.from_name`, this is an eager method that will hydrate the local object with metadata from Modal servers.
```
Model = modal.Cls.from_name("other-app", "Model")
model = Model()
model.inference(...)
```
 modal.Cls (https://modal.com/docs/reference/modal.Cls# modalcls)hydrate (https://modal.com/docs/reference/modal.Cls# hydrate)from_name (https://modal.com/docs/reference/modal.Cls# from_name)with_options (https://modal.com/docs/reference/modal.Cls# with_options)lookup (https://modal.com/docs/reference/modal.Cls# lookup)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)