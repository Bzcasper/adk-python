---
title: "Modal.Gpu"
url: "https://modal.com/docs/reference/modal.gpu"
date: "2025-04-15 01:06:34"
word_count: 1112
---

# Modal.Gpu

**Source:** [https://modal.com/docs/reference/modal.gpu](https://modal.com/docs/reference/modal.gpu)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1112

## Table of Contents

- [modal.gpu](#modalgpu)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.gpu <a id="modalgpu"></a>
* *GPU configuration shortcodes**
You can pass a wide range of `str` values for the `gpu` parameter of `@app.function` (https://modal.com/docs/reference/modal.App# function).
For instance: * `gpu="H100"` will attach 1 H100 GPU to each container * `gpu="L40S"` will attach 1 L40S GPU to each container * `gpu="T4:4"` will attach 4 T4 GPUs to each container You can see a list of Modal GPU options in the GPU docs (https://modal.com/docs/guide/gpu).
* *Example**
```
@app.function(gpu="A100-80GB:4")
def my_gpu_function():
  ... # This will have 4 A100-80GB with each container
```
 * *Deprecation notes**
An older deprecated way to configure GPU is also still supported, but will be removed in future versions of Modal. Examples: * `gpu=modal.gpu.H100()` will attach 1 H100 GPU to each container * `gpu=modal.gpu.T4(count=4)` will attach 4 T4 GPUs to each container * `gpu=modal.gpu.A100()` will attach 1 A100-40GB GPUs to each container * `gpu=modal.gpu.A100(size="80GB")` will attach 1 A100-80GB GPUs to each container ## modal.gpu.A100
```
class A100(modal.gpu._GPUConfig)
```
 GPU class.
The flagship data center GPU of the Ampere architecture. Available in 40GB and 80GB GPU memory configurations.
```
def __init__(
  self,
  *,
  count: int = 1, # Number of GPUs per container. Defaults to 1.
  size: Union[str, None] = None, # Select GB configuration of GPU device: "40GB" or "80GB". Defaults to "40GB".
):
```
 ## modal.gpu.A10G
```
class A10G(modal.gpu._GPUConfig)
```
 GPU class.
A mid-tier data center GPU based on the Ampere architecture, providing 24 GB of memory. A10G GPUs deliver up to 3.3x better ML training performance, 3x better ML inference performance, and 3x better graphics performance, in comparison to NVIDIA T4 GPUs.
```
def __init__(
  self,
  *,
  # Number of GPUs per container. Defaults to 1.
  # Useful if you have very large models that don't fit on a single GPU.
  count: int = 1,
):
```
 ## modal.gpu.Any
```
class Any(modal.gpu._GPUConfig)
```
 Selects any one of the GPU classes available within Modal, according to availability.
```
def __init__(self, *, count: int = 1):
```
 ## modal.gpu.H100
```
class H100(modal.gpu._GPUConfig)
```
 GPU class.
The flagship data center GPU of the Hopper architecture. Enhanced support for FP8 precision and a Transformer Engine that provides up to 4X faster training over the prior generation for GPT-3 (175B) models.
```
def __init__(
  self,
  *,
  # Number of GPUs per container. Defaults to 1.
  # Useful if you have very large models that don't fit on a single GPU.
  count: int = 1,
):
```
 ## modal.gpu.L4
```
class L4(modal.gpu._GPUConfig)
```
 GPU class.
A mid-tier data center GPU based on the Ada Lovelace architecture, providing 24GB of GPU memory. Includes RTX (ray tracing) support.
```
class A100(modal.gpu._GPUConfig)
```
0 ## modal.gpu.L40S
```
class A100(modal.gpu._GPUConfig)
```
1 GPU class.
The L40S is a data center GPU for the Ada Lovelace architecture. It has 48 GB of on-chip GDDR6 RAM and enhanced support for FP8 precision.
```
def __init__(
  self,
  *,
  # Number of GPUs per container. Defaults to 1.
  # Useful if you have very large models that don't fit on a single GPU.
  count: int = 1,
):
```
 ## modal.gpu.T4
```
class A100(modal.gpu._GPUConfig)
```
3 GPU class.
A low-cost data center GPU based on the Turing architecture, providing 16GB of GPU memory.
```
class A100(modal.gpu._GPUConfig)
```
0 ## modal.gpu.parse_gpu_config
```
class A100(modal.gpu._GPUConfig)
```
5 modal.gpu (https://modal.com/docs/reference/modal.gpu# modalgpu)modal.gpu.A100 (https://modal.com/docs/reference/modal.gpu# modalgpua100)modal.gpu.A10G (https://modal.com/docs/reference/modal.gpu# modalgpua10g)modal.gpu.Any (https://modal.com/docs/reference/modal.gpu# modalgpuany)modal.gpu.H100 (https://modal.com/docs/reference/modal.gpu# modalgpuh100)modal.gpu.L4 (https://modal.com/docs/reference/modal.gpu# modalgpul4)modal.gpu.L40S (https://modal.com/docs/reference/modal.gpu# modalgpul40s)modal.gpu.T4 (https://modal.com/docs/reference/modal.gpu# modalgput4)modal.gpu.parse_gpu_config (https://modal.com/docs/reference/modal.gpu# modalgpuparse_gpu_config)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)