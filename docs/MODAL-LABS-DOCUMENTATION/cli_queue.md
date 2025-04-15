---
title: "Queue"
url: "https://modal.com/docs/reference/cli/queue"
date: "2025-04-15 01:06:34"
word_count: 1256
---

# Queue

**Source:** [https://modal.com/docs/reference/cli/queue](https://modal.com/docs/reference/cli/queue)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1256

## Table of Contents

- [`modal queue`](#modal-queue)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# `modal queue` <a id="modal-queue"></a>
Manage `modal.Queue` objects and inspect their contents.
* *Usage** :
```
modal queue [OPTIONS] COMMAND [ARGS]...
```
 * *Options** : * `--help`: Show this message and exit. * *Commands** : * `create`: Create a named Queue. * `delete`: Delete a named Queue and all of its data. * `list`: List all named Queues. * `clear`: Clear the contents of a queue by removing all of its data. * `peek`: Print the next N items in the queue or queue partition (without removal). * `len`: Print the length of a queue partition or the total length of all partitions. ## `modal queue create`
Create a named Queue.
Note: This is a no-op when the Queue already exists.
* *Usage** :
```
modal queue create [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal queue delete`
Delete a named Queue and all of its data.
* *Usage** :
```
modal queue delete [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-y, --yes`: Run without pausing for confirmation. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal queue list`
List all named Queues.
* *Usage** :
```
modal queue list [OPTIONS]
```
 * *Options** : * `--json / --no-json`: [default: no-json] * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal queue clear`
Clear the contents of a queue by removing all of its data.
* *Usage** :
```
modal queue clear [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-p, --partition TEXT`: Name of the partition to use, otherwise use the default (anonymous) partition. * `-a, --all`: Clear the contents of all partitions. * `-y, --yes`: Run without pausing for confirmation. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal queue peek`
Print the next N items in the queue or queue partition (without removal).
* *Usage** :
```
modal queue peek [OPTIONS] NAME [N]
```
 * *Arguments** : * `NAME`: [required] * `[N]`: [default: 1] * *Options** : * `-p, --partition TEXT`: Name of the partition to use, otherwise use the default (anonymous) partition. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal queue len`
Print the length of a queue partition or the total length of all partitions.
* *Usage** :
```
modal queue len [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-p, --partition TEXT`: Name of the partition to use, otherwise use the default (anonymous) partition. * `-t, --total`: Compute the sum of the queue lengths across all partitions * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. modal queue (https://modal.com/docs/reference/cli/queue# modal-queue)modal queue create (https://modal.com/docs/reference/cli/queue# modal-queue-create)modal queue delete (https://modal.com/docs/reference/cli/queue# modal-queue-delete)modal queue list (https://modal.com/docs/reference/cli/queue# modal-queue-list)modal queue clear (https://modal.com/docs/reference/cli/queue# modal-queue-clear)modal queue peek (https://modal.com/docs/reference/cli/queue# modal-queue-peek)modal queue len (https://modal.com/docs/reference/cli/queue# modal-queue-len)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)