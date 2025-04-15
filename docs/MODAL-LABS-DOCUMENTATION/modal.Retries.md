---
title: "Modal.Retries"
url: "https://modal.com/docs/reference/modal.Retries"
date: "2025-04-15 01:06:34"
word_count: 688
---

# Modal.Retries

**Source:** [https://modal.com/docs/reference/modal.Retries](https://modal.com/docs/reference/modal.Retries)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 688

## Table of Contents

- [modal.Retries](#modalretries)
- [Basic configuration.](#basic-configuration)
- [This sets a policy of max 4 retries with 1-second delay between failures.](#this-sets-a-policy-of-max-4-retries-with-1-second-delay-between-failures)
- [Fixed-interval retries with 3-second delay between failures.](#fixed-interval-retries-with-3-second-delay-between-failures)
- [Exponential backoff, with retry delay doubling after each failure.](#exponential-backoff-with-retry-delay-doubling-after-each-failure)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Retries <a id="modalretries"></a>
```
class Retries(object)
```
 Adds a retry policy to a Modal function.
* *Usage**
```
import modal
app = modal.App()
# Basic configuration. <a id="basic-configuration"></a>
# This sets a policy of max 4 retries with 1-second delay between failures. <a id="this-sets-a-policy-of-max-4-retries-with-1-second-delay-between-failures"></a>
@app.function(retries=4)
def f():
  pass
# Fixed-interval retries with 3-second delay between failures. <a id="fixed-interval-retries-with-3-second-delay-between-failures"></a>
@app.function(
  retries=modal.Retries(
    max_retries=2,
    backoff_coefficient=1.0,
    initial_delay=3.0,
  )
)
def g():
  pass
# Exponential backoff, with retry delay doubling after each failure. <a id="exponential-backoff-with-retry-delay-doubling-after-each-failure"></a>
@app.function(
  retries=modal.Retries(
    max_retries=4,
    backoff_coefficient=2.0,
    initial_delay=1.0,
  )
)
def h():
  pass
```
```
def __init__(
  self,
  *,
  # The maximum number of retries that can be made in the presence of failures.
  max_retries: int,
  # Coefficent controlling how much the retry delay increases each retry attempt.
  # A backoff coefficient of 1.0 creates fixed-delay where the delay period always equals the initial delay.
  backoff_coefficient: float = 2.0,
  # Number of seconds that must elapse before the first retry occurs.
  initial_delay: float = 1.0,
  # Maximum length of retry delay in seconds, preventing the delay from growing infinitely.
  max_delay: float = 60.0,
):
```
 Construct a new retries policy, supporting exponential and fixed-interval delays via a backoff coefficient.
modal.Retries (https://modal.com/docs/reference/modal.Retries# modalretries)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)