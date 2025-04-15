---
title: "Modal.Function"
url: "https://modal.com/docs/reference/modal.Function"
date: "2025-04-15 01:06:34"
word_count: 1277
---

# Modal.Function

**Source:** [https://modal.com/docs/reference/modal.Function](https://modal.com/docs/reference/modal.Function)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1277

## Table of Contents

- [modal.Function](#modalfunction)
  - [keep_warm](#keepwarm)
- [Usage on a regular function.](#usage-on-a-regular-function)
- [Usage on a parametrized function.](#usage-on-a-parametrized-function)
  - [remote](#remote)
  - [remote_gen](#remotegen)
  - [local](#local)
  - [spawn](#spawn)
  - [get_raw_f](#getrawf)
  - [get_current_stats](#getcurrentstats)
  - [map](#map)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Function <a id="modalfunction"></a>
```
class Function(typing.Generic, modal.object.Object)
```
 Functions are the basic units of serverless execution on Modal.
Generally, you will not construct a `Function` directly. Instead, use the `App.function()` decorator to register your Python functions with your App.
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
## keep_warm <a id="keepwarm"></a>
```
@live_method
def keep_warm(self, warm_pool_size: int) -> None:
```
 Set the warm pool size for the function.
Please exercise care when using this advanced feature! Setting and forgetting a warm pool on functions can lead to increased costs.
```
# Usage on a regular function. <a id="usage-on-a-regular-function"></a>
f = modal.Function.from_name("my-app", "function")
f.keep_warm(2)
# Usage on a parametrized function. <a id="usage-on-a-parametrized-function"></a>
Model = modal.Cls.from_name("my-app", "Model")
Model("fine-tuned-model").keep_warm(2) # note that this applies to the class instance, not a method
```
 ## from_name
```
@classmethod
@renamed_parameter((2024, 12, 18), "tag", "name")
def from_name(
  cls: type["_Function"],
  app_name: str,
  name: str,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  environment_name: Optional[str] = None,
) -> "_Function":
```
 Reference a Function from a deployed App by its name.
In contrast to `modal.Function.lookup`, this is a lazy method that defers hydrating the local object with metadata from Modal servers until the first time it is actually used.
```
f = modal.Function.from_name("other-app", "function")
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
) -> "_Function":
```
 Lookup a Function from a deployed App by its name.
DEPRECATED: This method is deprecated in favor of `modal.Function.from_name`.
In contrast to `modal.Function.from_name`, this is an eager method that will hydrate the local object with metadata from Modal servers.
```
f = modal.Function.lookup("other-app", "function")
```
 ## web_url
```
@property
@live_method
def web_url(self) -> Optional[str]:
```
 URL of a Function running as a web endpoint.
## remote <a id="remote"></a>
```
def __init__(self, *args, **kwargs):
```
0 Calls the function remotely, executing it with the given arguments and returning the executions result.
## remote_gen <a id="remotegen"></a>
```
def __init__(self, *args, **kwargs):
```
1 Calls the generator remotely, executing it with the given arguments and returning the executions result.
## local <a id="local"></a>
```
def __init__(self, *args, **kwargs):
```
2 Calls the function locally, executing it with the given arguments and returning the executions result.
The function will execute in the same environment as the caller, just like calling the underlying function directly in Python. In particular, only secrets available in the caller environment will be available through environment variables.
## spawn <a id="spawn"></a>
```
def __init__(self, *args, **kwargs):
```
3 Calls the function with the given arguments, without waiting for the results.
Returns a `modal.FunctionCall` object, that can later be polled or waited for using `.get(timeout=...)`. Conceptually similar to `multiprocessing.pool.apply_async`, or a Future/Promise in other contexts.
## get_raw_f <a id="getrawf"></a>
```
def __init__(self, *args, **kwargs):
```
4 Return the inner Python object wrapped by this Modal Function.
## get_current_stats <a id="getcurrentstats"></a>
```
def __init__(self, *args, **kwargs):
```
5 Return a `FunctionStats` object describing the current functions queue and runner counts.
## map <a id="map"></a>
```
def __init__(self, *args, **kwargs):
```
6 Parallel map over a set of inputs.
Takes one iterator argument per argument in the function being mapped over.
Example:
```
def __init__(self, *args, **kwargs):
```
7 If applied to a `app.function`, `map()` returns one result per input and the output order is guaranteed to be the same as the input order. Set `order_outputs=False` to return results in the order that they are completed instead.
`return_exceptions` can be used to treat exceptions as successful results:
```
def __init__(self, *args, **kwargs):
```
8 ## starmap
```
def __init__(self, *args, **kwargs):
```
9 Like `map`, but spreads arguments over multiple function arguments.
Assumes every input is a sequence (e.g. a tuple).
Example:
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
0 ## for_each
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
1 Execute function for all inputs, ignoring outputs.
Convenient alias for `.map()` in cases where the function just needs to be called. as the caller doesnt have to consume the generator to process the inputs.
modal.Function (https://modal.com/docs/reference/modal.Function# modalfunction)hydrate (https://modal.com/docs/reference/modal.Function# hydrate)keep_warm (https://modal.com/docs/reference/modal.Function# keep_warm)from_name (https://modal.com/docs/reference/modal.Function# from_name)lookup (https://modal.com/docs/reference/modal.Function# lookup)web_url (https://modal.com/docs/reference/modal.Function# web_url)remote (https://modal.com/docs/reference/modal.Function# remote)remote_gen (https://modal.com/docs/reference/modal.Function# remote_gen)local (https://modal.com/docs/reference/modal.Function# local)spawn (https://modal.com/docs/reference/modal.Function# spawn)get_raw_f (https://modal.com/docs/reference/modal.Function# get_raw_f)get_current_stats (https://modal.com/docs/reference/modal.Function# get_current_stats)map (https://modal.com/docs/reference/modal.Function# map)starmap (https://modal.com/docs/reference/modal.Function# starmap)for_each (https://modal.com/docs/reference/modal.Function# for_each)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)