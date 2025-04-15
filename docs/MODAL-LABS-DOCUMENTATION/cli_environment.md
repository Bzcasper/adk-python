---
title: "Environment"
url: "https://modal.com/docs/reference/cli/environment"
date: "2025-04-15 01:06:34"
word_count: 998
---

# Environment

**Source:** [https://modal.com/docs/reference/cli/environment](https://modal.com/docs/reference/cli/environment)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 998

## Table of Contents

- [`modal environment`](#modal-environment)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# `modal environment` <a id="modal-environment"></a>
Create and interact with Environments
Environments are sub-divisons of workspaces, allowing you to deploy the same app in different namespaces. Each environment has their own set of Secrets and any lookups performed from an app in an environment will by default look for entities in the same environment.
Typical use cases for environments include having one for development and one for production, to prevent overwriting production apps when developing new features while still being able to deploy changes to a live environment.
* *Usage** :
```
modal environment [OPTIONS] COMMAND [ARGS]...
```
 * *Options** : * `--help`: Show this message and exit. * *Commands** : * `list`: List all environments in the current workspace * `create`: Create a new environment in the current workspace * `delete`: Delete an environment in the current workspace * `update`: Update the name or web suffix of an environment ## `modal environment list`
List all environments in the current workspace
* *Usage** :
```
modal environment list [OPTIONS]
```
 * *Options** : * `--json / --no-json`: [default: no-json] * `--help`: Show this message and exit. ## `modal environment create`
Create a new environment in the current workspace
* *Usage** :
```
modal environment create [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: Name of the new environment. Must be unique. Case sensitive [required] * *Options** : * `--help`: Show this message and exit. ## `modal environment delete`
Delete an environment in the current workspace
Deletes all apps in the selected environment and deletes the environment irrevocably.
* *Usage** :
```
modal environment delete [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: Name of the environment to be deleted. Case sensitive [required] * *Options** : * `--confirm / --no-confirm`: Set this flag to delete without prompting for confirmation [default: no-confirm] * `--help`: Show this message and exit. ## `modal environment update`
Update the name or web suffix of an environment
* *Usage** :
```
modal environment update [OPTIONS] CURRENT_NAME
```
 * *Arguments** : * `CURRENT_NAME`: [required] * *Options** : * `--set-name TEXT`: New name of the environment * `--set-web-suffix TEXT`: New web suffix of environment (empty string is no suffix) * `--help`: Show this message and exit. modal environment (https://modal.com/docs/reference/cli/environment# modal-environment)modal environment list (https://modal.com/docs/reference/cli/environment# modal-environment-list)modal environment create (https://modal.com/docs/reference/cli/environment# modal-environment-create)modal environment delete (https://modal.com/docs/reference/cli/environment# modal-environment-delete)modal environment update (https://modal.com/docs/reference/cli/environment# modal-environment-update)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)