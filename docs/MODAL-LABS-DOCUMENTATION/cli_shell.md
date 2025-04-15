---
title: "Shell"
url: "https://modal.com/docs/reference/cli/shell"
date: "2025-04-15 01:06:34"
word_count: 997
---

# Shell

**Source:** [https://modal.com/docs/reference/cli/shell](https://modal.com/docs/reference/cli/shell)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 997

## Table of Contents

- [`modal shell`](#modal-shell)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# `modal shell` <a id="modal-shell"></a>
Run a command or interactive shell inside a Modal container.
* *Examples:**
Start an interactive shell inside the default Debian-based image:
```
modal shell
```
 Start an interactive shell with the spec for `my_function` in your App (uses the same image, volumes, mounts, etc.):
```
modal shell hello_world.py::my_function
```
 Or, if youre using a modal.Cls (https://modal.com/docs/reference/modal.Cls), you can refer to a `@modal.method` directly:
```
modal shell hello_world.py::MyClass.my_method
```
 Start a `python` shell:
```
modal shell hello_world.py --cmd=python
```
 Run a command with your functions spec and pipe the output to a file:
```
modal shell hello_world.py -c 'uv pip list' > env.txt
```
 * *Usage** :
```
modal shell [OPTIONS] REF
```
 * *Arguments** : * `REF`: ID of running container, or path to a Python file containing a Modal App. Can also include a function specifier, like `module.py::func`, if the file defines multiple functions. * *Options** : * `-c, --cmd TEXT`: Command to run inside the Modal image. [default: /bin/bash] * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--image TEXT`: Container image tag for inside the shell (if not using REF). * `--add-python TEXT`: Add Python to the image (if not using REF). * `--volume TEXT`: Name of a `modal.Volume` to mount inside the shell at `/mnt/{name}` (if not using REF). Can be used multiple times. * `--cpu INTEGER`: Number of CPUs to allocate to the shell (if not using REF). * `--memory INTEGER`: Memory to allocate for the shell, in MiB (if not using REF). * `--gpu TEXT`: GPUs to request for the shell, if any. Examples are `any`, `a10g`, `a100:4` (if not using REF). * `--cloud TEXT`: Cloud provider to run the shell on. Possible values are `aws`, `gcp`, `oci`, `auto` (if not using REF). * `--region TEXT`: Region(s) to run the container on. Can be a single region or a comma-separated list to choose from (if not using REF). * `--pty / --no-pty`: Run the command using a PTY. * `-m`: Interpret argument as a Python module path instead of a file/script path * `--help`: Show this message and exit. modal shell (https://modal.com/docs/reference/cli/shell# modal-shell)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)