---
title: "Modal.Exception"
url: "https://modal.com/docs/reference/modal.exception"
date: "2025-04-15 01:06:34"
word_count: 1360
---

# Modal.Exception

**Source:** [https://modal.com/docs/reference/modal.exception](https://modal.com/docs/reference/modal.exception)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1360

## Table of Contents

- [modal.exception](#modalexception)
  - [modal.exception.AuthError](#modalexceptionautherror)
  - [modal.exception.ClientClosed](#modalexceptionclientclosed)
  - [modal.exception.DeprecationError](#modalexceptiondeprecationerror)
  - [modal.exception.DeserializationError](#modalexceptiondeserializationerror)
  - [modal.exception.ExecutionError](#modalexceptionexecutionerror)
  - [modal.exception.FilesystemExecutionError](#modalexceptionfilesystemexecutionerror)
  - [modal.exception.FunctionTimeoutError](#modalexceptionfunctiontimeouterror)
  - [modal.exception.InputCancellation](#modalexceptioninputcancellation)
  - [modal.exception.InteractiveTimeoutError](#modalexceptioninteractivetimeouterror)
  - [modal.exception.InternalFailure](#modalexceptioninternalfailure)
  - [modal.exception.InvalidError](#modalexceptioninvaliderror)
  - [modal.exception.ModuleNotMountable](#modalexceptionmodulenotmountable)
  - [modal.exception.NotFoundError](#modalexceptionnotfounderror)
  - [modal.exception.OutputExpiredError](#modalexceptionoutputexpirederror)
  - [modal.exception.PendingDeprecationError](#modalexceptionpendingdeprecationerror)
  - [modal.exception.RemoteError](#modalexceptionremoteerror)
  - [modal.exception.RequestSizeError](#modalexceptionrequestsizeerror)
  - [modal.exception.SandboxTerminatedError](#modalexceptionsandboxterminatederror)
  - [modal.exception.SandboxTimeoutError](#modalexceptionsandboxtimeouterror)
  - [modal.exception.SerializationError](#modalexceptionserializationerror)
  - [modal.exception.ServerWarning](#modalexceptionserverwarning)
  - [modal.exception.TimeoutError](#modalexceptiontimeouterror)
  - [modal.exception.VersionError](#modalexceptionversionerror)
  - [modal.exception.VolumeUploadTimeoutError](#modalexceptionvolumeuploadtimeouterror)
  - [modal.exception.simulate_preemption](#modalexceptionsimulatepreemption)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.exception <a id="modalexception"></a>
## modal.exception.AuthError <a id="modalexceptionautherror"></a>
```
class AuthError(modal.exception.Error)
```
 Raised when a client has missing or invalid authentication.
## modal.exception.ClientClosed <a id="modalexceptionclientclosed"></a>
```
class ClientClosed(modal.exception.Error)
```
 ## modal.exception.ConnectionError
```
class ConnectionError(modal.exception.Error)
```
 Raised when an issue occurs while connecting to the Modal servers.
## modal.exception.DeprecationError <a id="modalexceptiondeprecationerror"></a>
```
class DeprecationError(UserWarning)
```
 UserWarning category emitted when a deprecated Modal feature or API is used.
## modal.exception.DeserializationError <a id="modalexceptiondeserializationerror"></a>
```
class DeserializationError(modal.exception.Error)
```
 Raised to provide more context when an error is encountered during deserialization.
## modal.exception.ExecutionError <a id="modalexceptionexecutionerror"></a>
```
class ExecutionError(modal.exception.Error)
```
 Raised when something unexpected happened during runtime.
## modal.exception.FilesystemExecutionError <a id="modalexceptionfilesystemexecutionerror"></a>
```
class FilesystemExecutionError(modal.exception.Error)
```
 Raised when an unknown error is thrown during a container filesystem operation.
## modal.exception.FunctionTimeoutError <a id="modalexceptionfunctiontimeouterror"></a>
```
class FunctionTimeoutError(modal.exception.TimeoutError)
```
 Raised when a Function exceeds its execution duration limit and times out.
## modal.exception.InputCancellation <a id="modalexceptioninputcancellation"></a>
```
class InputCancellation(BaseException)
```
 Raised when the current input is cancelled by the task
Intentionally a BaseException instead of an Exception, so it wont get caught by unspecified user exception clauses that might be used for retries and other control flow.
## modal.exception.InteractiveTimeoutError <a id="modalexceptioninteractivetimeouterror"></a>
```
class InteractiveTimeoutError(modal.exception.TimeoutError)
```
 Raised when interactive frontends time out while trying to connect to a container.
## modal.exception.InternalFailure <a id="modalexceptioninternalfailure"></a>
```
class ClientClosed(modal.exception.Error)
```
0 Retriable internal error.
## modal.exception.InvalidError <a id="modalexceptioninvaliderror"></a>
```
class ClientClosed(modal.exception.Error)
```
1 Raised when user does something invalid.
## modal.exception.ModuleNotMountable <a id="modalexceptionmodulenotmountable"></a>
```
class ClientClosed(modal.exception.Error)
```
2 ## modal.exception.MountUploadTimeoutError
```
class ClientClosed(modal.exception.Error)
```
3 Raised when a Mount upload times out.
## modal.exception.NotFoundError <a id="modalexceptionnotfounderror"></a>
```
class ClientClosed(modal.exception.Error)
```
4 Raised when a requested resource was not found.
## modal.exception.OutputExpiredError <a id="modalexceptionoutputexpirederror"></a>
```
class ClientClosed(modal.exception.Error)
```
5 Raised when the Output exceeds expiration and times out.
## modal.exception.PendingDeprecationError <a id="modalexceptionpendingdeprecationerror"></a>
```
class ClientClosed(modal.exception.Error)
```
6 Soon to be deprecated feature. Only used intermittently because of multi-repo concerns.
## modal.exception.RemoteError <a id="modalexceptionremoteerror"></a>
```
class ClientClosed(modal.exception.Error)
```
7 Raised when an error occurs on the Modal server.
## modal.exception.RequestSizeError <a id="modalexceptionrequestsizeerror"></a>
```
class ClientClosed(modal.exception.Error)
```
8 Raised when an operation produces a gRPC request that is rejected by the server for being too large.
## modal.exception.SandboxTerminatedError <a id="modalexceptionsandboxterminatederror"></a>
```
class ClientClosed(modal.exception.Error)
```
9 Raised when a Sandbox is terminated for an internal reason.
## modal.exception.SandboxTimeoutError <a id="modalexceptionsandboxtimeouterror"></a>
```
class ConnectionError(modal.exception.Error)
```
0 Raised when a Sandbox exceeds its execution duration limit and times out.
## modal.exception.SerializationError <a id="modalexceptionserializationerror"></a>
```
class ConnectionError(modal.exception.Error)
```
1 Raised to provide more context when an error is encountered during serialization.
## modal.exception.ServerWarning <a id="modalexceptionserverwarning"></a>
```
class ConnectionError(modal.exception.Error)
```
2 Warning originating from the Modal server and re-issued in client code.
## modal.exception.TimeoutError <a id="modalexceptiontimeouterror"></a>
```
class ConnectionError(modal.exception.Error)
```
3 Base class for Modal timeouts.
## modal.exception.VersionError <a id="modalexceptionversionerror"></a>
```
class ConnectionError(modal.exception.Error)
```
4 Raised when the current client version of Modal is unsupported.
## modal.exception.VolumeUploadTimeoutError <a id="modalexceptionvolumeuploadtimeouterror"></a>
```
class ConnectionError(modal.exception.Error)
```
5 Raised when a Volume upload times out.
## modal.exception.simulate_preemption <a id="modalexceptionsimulatepreemption"></a>
```
class ConnectionError(modal.exception.Error)
```
6 Utility for simulating a preemption interrupt after `wait_seconds` seconds. The first interrupt is the SIGINT signal. After 30 seconds, a second interrupt will trigger.
This second interrupt simulates SIGKILL, and should not be caught. Optionally add between zero and `jitter_seconds` seconds of additional waiting before first interrupt.
* *Usage:**
```
class ConnectionError(modal.exception.Error)
```
7 See <https://modal.com/docs/guide/preemption> for more details on preemption handling.
modal.exception (https://modal.com/docs/reference/modal.exception# modalexception)modal.exception.AuthError (https://modal.com/docs/reference/modal.exception# modalexceptionautherror)modal.exception.ClientClosed (https://modal.com/docs/reference/modal.exception# modalexceptionclientclosed)modal.exception.ConnectionError (https://modal.com/docs/reference/modal.exception# modalexceptionconnectionerror)modal.exception.DeprecationError (https://modal.com/docs/reference/modal.exception# modalexceptiondeprecationerror)modal.exception.DeserializationError (https://modal.com/docs/reference/modal.exception# modalexceptiondeserializationerror)modal.exception.ExecutionError (https://modal.com/docs/reference/modal.exception# modalexceptionexecutionerror)modal.exception.FilesystemExecutionError (https://modal.com/docs/reference/modal.exception# modalexceptionfilesystemexecutionerror)modal.exception.FunctionTimeoutError (https://modal.com/docs/reference/modal.exception# modalexceptionfunctiontimeouterror)modal.exception.InputCancellation (https://modal.com/docs/reference/modal.exception# modalexceptioninputcancellation)modal.exception.InteractiveTimeoutError (https://modal.com/docs/reference/modal.exception# modalexceptioninteractivetimeouterror)modal.exception.InternalFailure (https://modal.com/docs/reference/modal.exception# modalexceptioninternalfailure)modal.exception.InvalidError (https://modal.com/docs/reference/modal.exception# modalexceptioninvaliderror)modal.exception.ModuleNotMountable (https://modal.com/docs/reference/modal.exception# modalexceptionmodulenotmountable)modal.exception.MountUploadTimeoutError (https://modal.com/docs/reference/modal.exception# modalexceptionmountuploadtimeouterror)modal.exception.NotFoundError (https://modal.com/docs/reference/modal.exception# modalexceptionnotfounderror)modal.exception.OutputExpiredError (https://modal.com/docs/reference/modal.exception# modalexceptionoutputexpirederror)modal.exception.PendingDeprecationError (https://modal.com/docs/reference/modal.exception# modalexceptionpendingdeprecationerror)modal.exception.RemoteError (https://modal.com/docs/reference/modal.exception# modalexceptionremoteerror)modal.exception.RequestSizeError (https://modal.com/docs/reference/modal.exception# modalexceptionrequestsizeerror)modal.exception.SandboxTerminatedError (https://modal.com/docs/reference/modal.exception# modalexceptionsandboxterminatederror)modal.exception.SandboxTimeoutError (https://modal.com/docs/reference/modal.exception# modalexceptionsandboxtimeouterror)modal.exception.SerializationError (https://modal.com/docs/reference/modal.exception# modalexceptionserializationerror)modal.exception.ServerWarning (https://modal.com/docs/reference/modal.exception# modalexceptionserverwarning)modal.exception.TimeoutError (https://modal.com/docs/reference/modal.exception# modalexceptiontimeouterror)modal.exception.VersionError (https://modal.com/docs/reference/modal.exception# modalexceptionversionerror)modal.exception.VolumeUploadTimeoutError (https://modal.com/docs/reference/modal.exception# modalexceptionvolumeuploadtimeouterror)modal.exception.simulate_preemption (https://modal.com/docs/reference/modal.exception# modalexceptionsimulate_preemption)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)