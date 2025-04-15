---
title: "Volume"
url: "https://modal.com/docs/reference/cli/volume"
date: "2025-04-15 01:06:34"
word_count: 1518
---

# Volume

**Source:** [https://modal.com/docs/reference/cli/volume](https://modal.com/docs/reference/cli/volume)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1518

## Table of Contents

- [`modal volume`](#modal-volume)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# `modal volume` <a id="modal-volume"></a>
Read and edit `modal.Volume` volumes.
Note: users of `modal.NetworkFileSystem` should use the `modal nfs` command instead.
* *Usage** :
```
modal volume [OPTIONS] COMMAND [ARGS]...
```
 * *Options** : * `--help`: Show this message and exit. * *Commands** : * `create`: Create a named, persistent modal.Volume. * `get`: Download files from a modal.Volume object. * `list`: List the details of all modal.Volume volumes in an Environment. * `ls`: List files and directories in a modal.Volume volume. * `put`: Upload a file or directory to a modal.Volume. * `rm`: Delete a file or directory from a modal.Volume. * `cp`: within a modal.Volume. * `delete`: Delete a named, persistent modal.Volume. * `rename`: Rename a modal.Volume. ## `modal volume create`
Create a named, persistent modal.Volume.
* *Usage** :
```
modal volume create [OPTIONS] NAME
```
 * *Arguments** : * `NAME`: [required] * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--version INTEGER`: VolumeFS version. (Experimental) * `--help`: Show this message and exit. ## `modal volume get`
Download files from a modal.Volume object.
If a folder is passed for REMOTE_PATH, the contents of the folder will be downloaded recursively, including all subdirectories.
* *Example**
```
modal volume get <volume_name> logs/april-12-1.txt
modal volume get <volume_name> / volume_data_dump
```
 Use - as LOCAL_DESTINATION to write file contents to standard output.
* *Usage** :
```
modal volume get [OPTIONS] VOLUME_NAME REMOTE_PATH [LOCAL_DESTINATION]
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `REMOTE_PATH`: [required] * `[LOCAL_DESTINATION]`: [default: .] * *Options** : * `--force / --no-force`: [default: no-force] * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal volume list`
List the details of all modal.Volume volumes in an Environment.
* *Usage** :
```
modal volume list [OPTIONS]
```
 * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--json / --no-json`: [default: no-json] * `--help`: Show this message and exit. ## `modal volume ls`
List files and directories in a modal.Volume volume.
* *Usage** :
```
modal volume ls [OPTIONS] VOLUME_NAME [PATH]
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `[PATH]`: [default: /] * *Options** : * `--json / --no-json`: [default: no-json] * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal volume put`
Upload a file or directory to a modal.Volume.
Remote parent directories will be created as needed.
Ending the REMOTE_PATH with a forward slash (/), its assumed to be a directory and the file will be uploaded with its current name under that directory.
* *Usage** :
```
modal volume put [OPTIONS] VOLUME_NAME LOCAL_PATH [REMOTE_PATH]
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `LOCAL_PATH`: [required] * `[REMOTE_PATH]`: [default: /] * *Options** : * `-f, --force`: Overwrite existing files. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal volume rm`
Delete a file or directory from a modal.Volume.
* *Usage** :
```
modal volume rm [OPTIONS] VOLUME_NAME REMOTE_PATH
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `REMOTE_PATH`: [required] * *Options** : * `-r, --recursive`: Delete directory recursively * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal volume cp` within a modal.Volume. source file to destination file or multiple source files to destination directory.
* *Usage** :
```
modal volume cp [OPTIONS] VOLUME_NAME PATHS...
```
 * *Arguments** : * `VOLUME_NAME`: [required] * `PATHS...`: [required] * *Options** : * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal volume delete`
Delete a named, persistent modal.Volume.
* *Usage** :
```
modal volume delete [OPTIONS] VOLUME_NAME
```
 * *Arguments** : * `VOLUME_NAME`: Name of the modal.Volume to be deleted. Case sensitive [required] * *Options** : * `-y, --yes`: Run without pausing for confirmation. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. ## `modal volume rename`
Rename a modal.Volume.
* *Usage** :
```
modal volume create [OPTIONS] NAME
```
0 * *Arguments** : * `OLD_NAME`: [required] * `NEW_NAME`: [required] * *Options** : * `-y, --yes`: Run without pausing for confirmation. * `-e, --env TEXT`: Environment to interact with. If not specified, Modal will use the default environment of your current profile, or the `MODAL_ENVIRONMENT` variable. Otherwise, raises an error if the workspace has multiple environments. * `--help`: Show this message and exit. modal volume (https://modal.com/docs/reference/cli/volume# modal-volume)modal volume create (https://modal.com/docs/reference/cli/volume# modal-volume-create)modal volume get (https://modal.com/docs/reference/cli/volume# modal-volume-get)modal volume list (https://modal.com/docs/reference/cli/volume# modal-volume-list)modal volume ls (https://modal.com/docs/reference/cli/volume# modal-volume-ls)modal volume put (https://modal.com/docs/reference/cli/volume# modal-volume-put)modal volume rm (https://modal.com/docs/reference/cli/volume# modal-volume-rm)modal volume cp (https://modal.com/docs/reference/cli/volume# modal-volume-cp)modal volume delete (https://modal.com/docs/reference/cli/volume# modal-volume-delete)modal volume rename (https://modal.com/docs/reference/cli/volume# modal-volume-rename)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)