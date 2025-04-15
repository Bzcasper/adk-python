---
title: "Dict"
url: "https://modal.com/docs/reference/cli/dict"
date: "2025-04-15 01:06:34"
word_count: 1251
---

# Dict

**Source:** [https://modal.com/docs/reference/cli/dict](https://modal.com/docs/reference/cli/dict)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1251

## Table of Contents

- [`modal dict`](#modal-dict)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# `modal dict` <a id="modal-dict"></a>
Manage `modal.Dict` objects and inspect their contents.
* *Usage** :
```
modal dict [OPTIONS] COMMAND [ARGS]...
```
 * *Options** : * `--help`: Show this message and exit. * *Commands** : * `create`: Create a named Dict object. * `list`: List all named Dicts. * `clear`: Clear the contents of a named Dict by deleting all of its data. * `delete`: Delete a named Dict and all of its data. * `get`: Print the value for a specific key. * `items`: Print the contents of a Dict. ## `modal dict create`
Create a named Dict object.
Note: This is a no-op when the Dict already exists.
* *Usage** :
```
modal dict create [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal dict list`
List all named Dicts.
* *Usage** :
```
modal dict list [OPTIONS]
```
 * *Options** : * `--json / --no-json`: [default: no-json] * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal dict clear`
Clear the contents of a named Dict by deleting all of its data.
* *Usage** :
```
modal dict clear [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-y, --yes`: Run without pausing for confirmation. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal dict delete`
Delete a named Dict and all of its data.
* *Usage** :
```
modal dict delete [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-y, --yes`: Run without pausing for confirmation. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal dict get`
Print the value for a specific key.
Note: When using the CLI, keys are always interpreted as having a string type.
* *Usage** :
```
modal dict get [OPTIONS] NAME KEY
```
 * *Arguments** : * `NAME`: [required] * `KEY`: [required] * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal dict items`
Print the contents of a Dict.
Note: By default, this command truncates the contents. Use the `N` argument to control the amount of data shown or the `--all` option to retrieve the entire Dict, which may be slow.
* *Usage** :
```
modal dict items [OPTIONS] NAME [N]
```
 * *Arguments** : * `NAME`: [required] * `[N]`: Limit the number of entries shown [default: 20] * *Options** : * `-a, --all`: Ignore N and print all entries in the Dict (may be slow) * `-r, --repr`: Display items using `repr()` to see more details * `--json / --no-json`: [default: no-json] * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. modal dict (https://modal.com/docs/reference/cli/dict# modal-dict)modal dict create (https://modal.com/docs/reference/cli/dict# modal-dict-create)modal dict list (https://modal.com/docs/reference/cli/dict# modal-dict-list)modal dict clear (https://modal.com/docs/reference/cli/dict# modal-dict-clear)modal dict delete (https://modal.com/docs/reference/cli/dict# modal-dict-delete)modal dict get (https://modal.com/docs/reference/cli/dict# modal-dict-get)modal dict items (https://modal.com/docs/reference/cli/dict# modal-dict-items)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)