---
title: "Modal.Config"
url: "https://modal.com/docs/reference/modal.config"
date: "2025-04-15 01:06:34"
word_count: 1302
---

# Modal.Config

**Source:** [https://modal.com/docs/reference/modal.config](https://modal.com/docs/reference/modal.config)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1302

## Table of Contents

- [modal.config](#modalconfig)
  - [Setting tokens using the CLI](#setting-tokens-using-the-cli)
  - [Other configuration options](#other-configuration-options)
  - [modal.config.config_set_active_profile](#modalconfigconfigsetactiveprofile)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.config <a id="modalconfig"></a>
Modal intentionally keeps configurability to a minimum.
The main configuration options are the API tokens: the token id and the token secret. These can be configured in two ways: 1. By running the `modal token set` command. This writes the tokens to `.modal.toml` file in your home directory. 2. By setting the environment variables `MODAL_TOKEN_ID` and `MODAL_TOKEN_SECRET`. This takes precedence over the previous method. ## .modal.toml
The `.modal.toml` file is generally stored in your home directory. It should look like this::
```
[default]
token_id = "ak-12345..."
token_secret = "as-12345..."
```
 You can create this file manually, or you can run the `modal token set ...` command (see below).
## Setting tokens using the CLI <a id="setting-tokens-using-the-cli"></a>
You can set a token by running the command::
```
modal token set \
 --token-id <token id> \
 --token-secret <token secret>
```
 This will write the token id and secret to `.modal.toml`.
If the token id or secret is provided as the string `-` (a single dash), then it will be read in a secret way from stdin instead.
## Other configuration options <a id="other-configuration-options"></a>
Other possible configuration options are: * `loglevel` (in the .toml file) / `MODAL_LOGLEVEL` (as an env var). Defaults to `WARNING`. Set this to `DEBUG` to see internal messages. * `logs_timeout` (in the .toml file) / `MODAL_LOGS_TIMEOUT` (as an env var). Defaults to 10. Number of seconds to wait for logs to drain when closing the session, before giving up. * `automount` (in the .toml file) / `MODAL_AUTOMOUNT` (as an env var). Defaults to True. By default, Modal automatically mounts modules imported in the current scope, that are deemed to be local. This can be turned off by setting this to False. * `force_build` (in the .toml file) / `MODAL_FORCE_BUILD` (as an env var). Defaults to False. When set, ignores the Image cache and builds all Image layers. Note that this will break the cache for all images based on the rebuilt layers, so other images may rebuild on subsequent runs / deploys even if the config is reverted. * `ignore_cache` (in the .toml file) / `MODAL_IGNORE_CACHE` (as an env var). Defaults to False. When set, ignores the Image cache and builds all Image layers. Unlike `force_build`, this will not overwrite the cache for other images that have the same recipe. Subsequent runs that do not use this option will pull the _previous_ Image from the cache, if one exists. It can be useful for testing an Apps robustness to Image rebuilds without clobbering Images used by other Apps. * `traceback` (in the .toml file) / `MODAL_TRACEBACK` (as an env var). Defaults to False. Enables printing full tracebacks on unexpected CLI errors, which can be useful for debugging client issues. ## Meta-configuration
Some meta-options are set using environment variables only: * `MODAL_CONFIG_PATH` lets you override the location of the .toml file, by default `~/.modal.toml`. * `MODAL_PROFILE` lets you use multiple sections in the .toml file and switch between them. It defaults to default. ## modal.config.Config
```
class Config(object)
```
 Singleton that holds configuration used by Modal internally.
```
def __init__(self):
```
 ### get
```
def get(self, key, profile=None, use_env=True):
```
 Looks up a configuration value.
Will check (in decreasing order of priority): 1. Any environment variable of the form MODAL_FOO_BAR (when use_env is True) 2. Settings in the users .toml configuration file 3. The default value of the setting ### override_locally
```
def override_locally(self, key: str, value: str):
  # Override setting in this process by overriding environment variable for the setting
  #
  # Does NOT write back to settings file etc.
```
 ### to_dict
```
def to_dict(self):
```
 ## modal.config.config_profiles
```
def config_profiles():
```
 List the available modal profiles in the .modal.toml file.
## modal.config.config_set_active_profile <a id="modalconfigconfigsetactiveprofile"></a>
```
def config_set_active_profile(env: str) -> None:
```
 Set the users active modal profile by writing it to the `.modal.toml` file.
modal.config (https://modal.com/docs/reference/modal.config# modalconfig).modal.toml (https://modal.com/docs/reference/modal.config# modaltoml)Setting tokens using the CLI (https://modal.com/docs/reference/modal.config# setting-tokens-using-the-cli)Other configuration options (https://modal.com/docs/reference/modal.config# other-configuration-options)Meta-configuration (https://modal.com/docs/reference/modal.config# meta-configuration)modal.config.Config (https://modal.com/docs/reference/modal.config# modalconfigconfig)get (https://modal.com/docs/reference/modal.config# get)override_locally (https://modal.com/docs/reference/modal.config# override_locally)to_dict (https://modal.com/docs/reference/modal.config# to_dict)modal.config.config_profiles (https://modal.com/docs/reference/modal.config# modalconfigconfig_profiles)modal.config.config_set_active_profile (https://modal.com/docs/reference/modal.config# modalconfigconfig_set_active_profile)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)