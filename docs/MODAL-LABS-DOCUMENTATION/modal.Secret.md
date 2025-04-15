---
title: "Modal.Secret"
url: "https://modal.com/docs/reference/modal.Secret"
date: "2025-04-15 01:06:34"
word_count: 990
---

# Modal.Secret

**Source:** [https://modal.com/docs/reference/modal.Secret](https://modal.com/docs/reference/modal.Secret)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 990

## Table of Contents

- [modal.Secret](#modalsecret)
  - [from_dict](#fromdict)
  - [from_dotenv](#fromdotenv)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Secret <a id="modalsecret"></a>
```
class Secret(modal.object.Object)
```
 Secrets provide a dictionary of environment variables for images.
Secrets are a secure way to add credentials and other sensitive information to the containers your functions run in. You can create and edit secrets on the dashboard (https://modal.com/secrets), or programmatically from Python code.
See the secrets guide page (https://modal.com/docs/guide/secrets) for more information.
```
def __init__(self, *args, **kwargs):
```
 ## hydrate
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
 Synchronize the local object with its identity on the Modal server.
It is rarely necessary to call this method explicitly, as most operations will lazily hydrate when needed. The main use case is when you need to access object metadata, such as its ID.
_Added in v0.72.39_ : This method replaces the deprecated `.resolve()` method.
## from_dict <a id="fromdict"></a>
```
@staticmethod
def from_dict(
  env_dict: dict[
    str, Union[str, None]
  ] = {}, # dict of entries to be inserted as environment variables in functions using the secret
):
```
 Create a secret from a str-str dictionary. Values can also be `None`, which is ignored.
Usage:
```
@app.function(secrets=[modal.Secret.from_dict({"FOO": "bar"})])
def run():
  print(os.environ["FOO"])
```
 ## from_local_environ
```
@staticmethod
def from_local_environ(
  env_keys: list[str], # list of local env vars to be included for remote execution
):
```
 Create secrets from local environment variables automatically.
## from_dotenv <a id="fromdotenv"></a>
```
@staticmethod
def from_dotenv(path=None, *, filename=".env"):
```
 Create secrets from a .env file automatically.
If no argument is provided, it will use the current working directory as the starting point for finding a `.env` file. Note that it does not use the location of the module calling `Secret.from_dotenv`.
If called with an argument, it will use that as a starting point for finding `.env` files. In particular, you can call it like this:
```
@app.function(secrets=[modal.Secret.from_dotenv(__file__)])
def run():
  print(os.environ["USERNAME"]) # Assumes USERNAME is defined in your .env file
```
 This will use the location of the script calling `modal.Secret.from_dotenv` as a starting point for finding the `.env` file.
A file named `.env` is expected by default, but this can be overridden with the `filename` keyword argument:
```
@app.function(secrets=[modal.Secret.from_dotenv(filename=".env-dev")])
def run():
  ...
```
 ## from_name
```
@staticmethod
@renamed_parameter((2024, 12, 18), "label", "name")
def from_name(
  name: str,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  environment_name: Optional[str] = None,
  required_keys: list[
    str
  ] = [], # Optionally, a list of required environment variables (will be asserted server-side)
) -> "_Secret":
```
 Reference a Secret by its name.
In contrast to most other Modal objects, named Secrets must be provisioned from the Dashboard. See other methods for alternate ways of creating a new Secret from code.
```
def __init__(self, *args, **kwargs):
```
0 modal.Secret (https://modal.com/docs/reference/modal.Secret# modalsecret)hydrate (https://modal.com/docs/reference/modal.Secret# hydrate)from_dict (https://modal.com/docs/reference/modal.Secret# from_dict)from_local_environ (https://modal.com/docs/reference/modal.Secret# from_local_environ)from_dotenv (https://modal.com/docs/reference/modal.Secret# from_dotenv)from_name (https://modal.com/docs/reference/modal.Secret# from_name)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)