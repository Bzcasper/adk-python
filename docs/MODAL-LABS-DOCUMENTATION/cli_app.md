---
title: "App"
url: "https://modal.com/docs/reference/cli/app"
date: "2025-04-15 01:06:34"
word_count: 1225
---

# App

**Source:** [https://modal.com/docs/reference/cli/app](https://modal.com/docs/reference/cli/app)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1225

## Table of Contents

- [`modal app`](#modal-app)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# `modal app` <a id="modal-app"></a>
Manage deployed and running apps.
* *Usage** :
```
modal app [OPTIONS] COMMAND [ARGS]...
```
 * *Options** : * `--help`: Show this message and exit. * *Commands** : * `list`: List Modal apps that are currently deployed/running or recently stopped. * `logs`: Show App logs, streaming while active. * `rollback`: Redeploy a previous version of an App. * `stop`: Stop an app. * `history`: Show App deployment history, for a currently deployed app ## `modal app list`
List Modal apps that are currently deployed/running or recently stopped.
* *Usage** :
```
modal app list [OPTIONS]
```
 * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--json / --no-json`: [default: no-json] * `--help`: Show this message and exit. ## `modal app logs`
Show App logs, streaming while active.
* *Examples:**
Get the logs based on an app ID:
```
modal app logs ap-123456
```
 Get the logs for a currently deployed App based on its name:
```
modal app logs my-app
```
 * *Usage** :
```
modal app logs [OPTIONS] [APP_IDENTIFIER]
```
 * *Arguments** : * `[APP_IDENTIFIER]`: App name or ID * *Options** : * `-n, --name TEXT`: Deprecated: Pass App name as a positional argument * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal app rollback`
Redeploy a previous version of an App.
Note that the App must currently be in a deployed state. Rollbacks will appear as a new deployment in the App history, although the App state will be reset to the state at the time of the previous deployment.
* *Examples:**
Rollback an App to its previous version:
```
modal app rollback my-app
```
 Rollback an App to a specific version:
```
modal app rollback my-app v3
```
 Rollback an App using its App ID instead of its name:
```
modal app rollback ap-abcdefghABCDEFGH123456
```
 * *Usage** :
```
modal app rollback [OPTIONS] [APP_IDENTIFIER] [VERSION]
```
 * *Arguments** : * `[APP_IDENTIFIER]`: App name or ID * `[VERSION]`: Target version for rollback. * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal app stop`
Stop an app.
* *Usage** :
```
modal app stop [OPTIONS] [APP_IDENTIFIER]
```
 * *Arguments** : * `[APP_IDENTIFIER]`: App name or ID * *Options** : * `-n, --name TEXT`: Deprecated: Pass App name as a positional argument * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal app history`
Show App deployment history, for a currently deployed app
* *Examples:**
Get the history based on an app ID:
```
modal app list [OPTIONS]
```
0 Get the history for a currently deployed App based on its name:
```
modal app list [OPTIONS]
```
1 * *Usage** :
```
modal app list [OPTIONS]
```
2 * *Arguments** : * `[APP_IDENTIFIER]`: App name or ID * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `-n, --name TEXT`: Deprecated: Pass App name as a positional argument * `--json / --no-json`: [default: no-json] * `--help`: Show this message and exit. modal app (https://modal.com/docs/reference/cli/app# modal-app)modal app list (https://modal.com/docs/reference/cli/app# modal-app-list)modal app logs (https://modal.com/docs/reference/cli/app# modal-app-logs)modal app rollback (https://modal.com/docs/reference/cli/app# modal-app-rollback)modal app stop (https://modal.com/docs/reference/cli/app# modal-app-stop)modal app history (https://modal.com/docs/reference/cli/app# modal-app-history)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)