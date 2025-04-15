---
title: "Nfs"
url: "https://modal.com/docs/reference/cli/nfs"
date: "2025-04-15 01:06:34"
word_count: 1340
---

# Nfs

**Source:** [https://modal.com/docs/reference/cli/nfs](https://modal.com/docs/reference/cli/nfs)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1340

## Table of Contents

- [`modal nfs`](#modal-nfs)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# `modal nfs` <a id="modal-nfs"></a>
Read and edit `modal.NetworkFileSystem` file systems.
* *Usage** :
```
modal nfs [OPTIONS] COMMAND [ARGS]...
```
 * *Options** : * `--help`: Show this message and exit. * *Commands** : * `list`: List the names of all network file systems. * `create`: Create a named network file system. * `ls`: List files and directories in a network file system. * `put`: Upload a file or directory to a network file system. * `get`: Download a file from a network file system. * `rm`: Delete a file or directory from a network file system. * `delete`: Delete a named, persistent modal.NetworkFileSystem. ## `modal nfs list`
List the names of all network file systems.
* *Usage** :
```
modal nfs list [OPTIONS]
```
 * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--json / --no-json`: [default: no-json] * `--help`: Show this message and exit. ## `modal nfs create`
Create a named network file system.
* *Usage** :
```
modal nfs create [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal nfs ls`
List files and directories in a network file system.
* *Usage** :
```
modal nfs ls [OPTIONS] VOLUME_NAME [PATH]
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `[PATH]`: [default: /] * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal nfs put`
Upload a file or directory to a network file system.
Remote parent directories will be created as needed.
Ending the REMOTE_PATH with a forward slash (/), its assumed to be a directory and the file will be uploaded with its current name under that directory.
* *Usage** :
```
modal nfs put [OPTIONS] VOLUME_NAME LOCAL_PATH [REMOTE_PATH]
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `LOCAL_PATH`: [required] * `[REMOTE_PATH]`: [default: /] * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal nfs get`
Download a file from a network file system.
Specifying a glob pattern (using any `*` or `**` patterns) as the `remote_path` will download all matching files, preserving their directory structure.
For example, to download an entire network file system into `dump_volume`:
```
modal nfs get <volume-name> "**" dump_volume
```
 Use - as LOCAL_DESTINATION to write file contents to standard output.
* *Usage** :
```
modal nfs get [OPTIONS] VOLUME_NAME REMOTE_PATH [LOCAL_DESTINATION]
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `REMOTE_PATH`: [required] * `[LOCAL_DESTINATION]`: [default: .] * *Options** : * `--force / --no-force`: [default: no-force] * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal nfs rm`
Delete a file or directory from a network file system.
* *Usage** :
```
modal nfs rm [OPTIONS] VOLUME_NAME REMOTE_PATH
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `REMOTE_PATH`: [required] * *Options** : * `-r, --recursive`: Delete directory recursively * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal nfs delete`
Delete a named, persistent modal.NetworkFileSystem.
* *Usage** :
```
modal nfs delete [OPTIONS] NFS_NAME
```
 * *Arguments** : * `NFS_NAME`: Name of the modal.NetworkFileSystem to be deleted. Case sensitive [required] * *Options** : * `-y, --yes`: Run without pausing for confirmation. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. modal nfs (https://modal.com/docs/reference/cli/nfs# modal-nfs)modal nfs list (https://modal.com/docs/reference/cli/nfs# modal-nfs-list)modal nfs create (https://modal.com/docs/reference/cli/nfs# modal-nfs-create)modal nfs ls (https://modal.com/docs/reference/cli/nfs# modal-nfs-ls)modal nfs put (https://modal.com/docs/reference/cli/nfs# modal-nfs-put)modal nfs get (https://modal.com/docs/reference/cli/nfs# modal-nfs-get)modal nfs rm (https://modal.com/docs/reference/cli/nfs# modal-nfs-rm)modal nfs delete (https://modal.com/docs/reference/cli/nfs# modal-nfs-delete)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)