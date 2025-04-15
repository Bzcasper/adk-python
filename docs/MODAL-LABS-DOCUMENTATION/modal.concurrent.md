---
title: "Modal.Concurrent"
url: "https://modal.com/docs/reference/modal.concurrent"
date: "2025-04-15 01:06:34"
word_count: 827
---

# Modal.Concurrent

**Source:** [https://modal.com/docs/reference/modal.concurrent](https://modal.com/docs/reference/modal.concurrent)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 827

## Table of Contents

- [modal.concurrent](#modalconcurrent)
- [Stack the decorator under `@app.function()` to enable input concurrency](#stack-the-decorator-under-appfunction-to-enable-input-concurrency)
- [With `@app.cls()`, apply the decorator at the class level, not on individual methods](#with-appcls-apply-the-decorator-at-the-class-level-not-on-individual-methods)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.concurrent <a id="modalconcurrent"></a>
```
def concurrent(
  _warn_parentheses_missing=None,
  *,
  max_inputs: int, # Hard limit on each container's input concurrency
  target_inputs: Optional[int] = None, # Input concurrency that Modal's autoscaler should target
) -> Callable[
  [Union[Callable[P, ReturnType], _PartialFunction[P, ReturnType, ReturnType]]],
  _PartialFunction[P, ReturnType, ReturnType],
]:
```
 Decorator that allows individual containers to handle multiple inputs concurrently.
The concurrency mechanism depends on whether the function is async or not: * Async functions will run inputs on a single thread as asyncio tasks. * Synchronous functions will use multi-threading. The code must be thread-safe. Input concurrency will be most useful for workflows that are IO-bound (e.g., making network requests) or when running an inference server that supports dynamic batching.
When `target_inputs` is set, Modals autoscaler will try to provision resources such that each container is running that many inputs concurrently, rather than autoscaling based on `max_inputs`. Containers may burst up to up to `max_inputs` if resources are insufficient to remain at the target concurrency, e.g. when the arrival rate of inputs increases. This can trade-off a small increase in average latency to avoid larger tail latencies from input queuing.
* *Examples:**
```
# Stack the decorator under `@app.function()` to enable input concurrency <a id="stack-the-decorator-under-appfunction-to-enable-input-concurrency"></a>
@app.function()
@modal.concurrent(max_inputs=100)
async def f(data):
  # Async function; will be scheduled as asyncio task
  ...
# With `@app.cls()`, apply the decorator at the class level, not on individual methods <a id="with-appcls-apply-the-decorator-at-the-class-level-not-on-individual-methods"></a>
@app.cls()
@modal.concurrent(max_inputs=100, target_inputs=80)
class C:
  @modal.method()
  def f(self, data):
    # Sync function; must be thread-safe
    ...
```
 _Added in v0.73.148:_ This decorator replaces the `allow_concurrent_inputs` parameter in `@app.function()` and `@app.cls()`.
modal.concurrent (https://modal.com/docs/reference/modal.concurrent# modalconcurrent)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)