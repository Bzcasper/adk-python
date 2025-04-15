---
title: "Modal.Functioncall"
url: "https://modal.com/docs/reference/modal.FunctionCall"
date: "2025-04-15 01:06:34"
word_count: 1091
---

# Modal.Functioncall

**Source:** [https://modal.com/docs/reference/modal.FunctionCall](https://modal.com/docs/reference/modal.FunctionCall)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1091

## Table of Contents

- [modal.FunctionCall](#modalfunctioncall)
  - [get](#get)
  - [get_gen](#getgen)
  - [get_call_graph](#getcallgraph)
  - [cancel](#cancel)
  - [from_id](#fromid)
- [Spawn a FunctionCall and keep track of its object ID](#spawn-a-functioncall-and-keep-track-of-its-object-id)
- [Later, use the ID to re-instantiate the FunctionCall object](#later-use-the-id-to-re-instantiate-the-functioncall-object)
  - [gather](#gather)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.FunctionCall <a id="modalfunctioncall"></a>
```
class FunctionCall(typing.Generic, modal.object.Object)
```
 A reference to an executed function call.
Constructed using `.spawn(...)` on a Modal function with the same arguments that a function normally takes. Acts as a reference to an ongoing function call that can be passed around and used to poll or fetch function results at some later time.
Conceptually similar to a Future/Promise/AsyncResult in other contexts and languages.
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
## get <a id="get"></a>
```
def get(self, timeout: Optional[float] = None) -> ReturnType:
```
 Get the result of the function call.
This function waits indefinitely by default. It takes an optional `timeout` argument that specifies the maximum number of seconds to wait, which can be set to `0` to poll for an output immediately.
The returned coroutine is not cancellation-safe.
## get_gen <a id="getgen"></a>
```
def get_gen(self) -> AsyncGenerator[Any, None]:
```
 Calls the generator remotely, executing it with the given arguments and returning the executions result.
## get_call_graph <a id="getcallgraph"></a>
```
def get_call_graph(self) -> list[InputInfo]:
```
 Returns a structure representing the call graph from a given root call ID, along with the status of execution for each node.
See `modal.call_graph` (https://modal.com/docs/reference/modal.call_graph) reference page for documentation on the structure of the returned `InputInfo` items.
## cancel <a id="cancel"></a>
```
def cancel(
  self,
  # if true, containers running the inputs are forcibly terminated
  terminate_containers: bool = False,
):
```
 Cancels the function call, which will stop its execution and mark its inputs as `TERMINATED` (https://modal.com/docs/reference/modal.call_graph# modalcall_graphinputstatus).
If `terminate_containers=True` - the containers running the cancelled inputs are all terminated causing any non-cancelled inputs on those containers to be rescheduled in new containers.
## from_id <a id="fromid"></a>
```
@staticmethod
def from_id(
  function_call_id: str, client: Optional[_Client] = None, is_generator: bool = False
) -> "_FunctionCall[Any]":
```
 Instantiate a FunctionCall object from an existing ID.
Examples:
```
# Spawn a FunctionCall and keep track of its object ID <a id="spawn-a-functioncall-and-keep-track-of-its-object-id"></a>
fc = my_func.spawn()
fc_id = fc.object_id
# Later, use the ID to re-instantiate the FunctionCall object <a id="later-use-the-id-to-re-instantiate-the-functioncall-object"></a>
fc = _FunctionCall.from_id(fc_id)
result = fc.get()
```
 Note that its only necessary to re-instantiate the `FunctionCall` with this method if you no longer have access to the original object returned from `Function.spawn`.
## gather <a id="gather"></a>
```
@staticmethod
def gather(*function_calls: "_FunctionCall[Any]") -> list[Any]:
```
 Wait until all Modal FunctionCall objects have results before returning.
Accepts a variable number of `FunctionCall` objects, as returned by `Function.spawn()`.
Returns a list of results from each FunctionCall, or raises an exception from the first failing function call.
Examples:
```
def __init__(self, *args, **kwargs):
```
0 _Added in v0.73.69_ : This method replaces the deprecated `modal.functions.gather` function.
modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall# modalfunctioncall)hydrate (https://modal.com/docs/reference/modal.FunctionCall# hydrate)get (https://modal.com/docs/reference/modal.FunctionCall# get)get_gen (https://modal.com/docs/reference/modal.FunctionCall# get_gen)get_call_graph (https://modal.com/docs/reference/modal.FunctionCall# get_call_graph)cancel (https://modal.com/docs/reference/modal.FunctionCall# cancel)from_id (https://modal.com/docs/reference/modal.FunctionCall# from_id)gather (https://modal.com/docs/reference/modal.FunctionCall# gather)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)