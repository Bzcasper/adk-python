---
title: "Modal.Sandbox"
url: "https://modal.com/docs/reference/modal.Sandbox"
date: "2025-04-15 01:06:34"
word_count: 1269
---

# Modal.Sandbox

**Source:** [https://modal.com/docs/reference/modal.Sandbox](https://modal.com/docs/reference/modal.Sandbox)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1269

## Table of Contents

- [modal.Sandbox](#modalsandbox)
  - [create](#create)
  - [set_tags](#settags)
  - [snapshot_filesystem](#snapshotfilesystem)
  - [wait](#wait)
  - [tunnels](#tunnels)
  - [terminate](#terminate)
  - [poll](#poll)
  - [exec](#exec)
  - [mkdir](#mkdir)
  - [rm](#rm)
  - [watch](#watch)
  - [stderr](#stderr)
  - [stdin](#stdin)
  - [returncode](#returncode)
  - [list](#list)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Sandbox <a id="modalsandbox"></a>
```
class Sandbox(modal.object.Object)
```
 A `Sandbox` object lets you interact with a running sandbox. This API is similar to Pythons .
Refer to the guide (https://modal.com/docs/guide/sandbox) on how to spawn and use sandboxes.
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
## create <a id="create"></a>
```
@staticmethod
def create(
  *entrypoint_args: str,
  app: Optional["modal.app._App"] = None, # Optionally associate the sandbox with an app
  environment_name: Optional[str] = None, # Optionally override the default environment
  image: Optional[_Image] = None, # The image to run as the container for the sandbox.
  mounts: Sequence[_Mount] = (), # Mounts to attach to the sandbox.
  secrets: Sequence[_Secret] = (), # Environment variables to inject into the sandbox.
  network_file_systems: dict[Union[str, os.PathLike], _NetworkFileSystem] = {},
  timeout: Optional[int] = None, # Maximum execution time of the sandbox in seconds.
  workdir: Optional[str] = None, # Working directory of the sandbox.
  gpu: GPU_T = None,
  cloud: Optional[str] = None,
  region: Optional[Union[str, Sequence[str]]] = None, # Region or regions to run the sandbox on.
  # Specify, in fractional CPU cores, how many CPU cores to request.
  # Or, pass (request, limit) to additionally specify a hard limit in fractional CPU cores.
  # CPU throttling will prevent a container from exceeding its specified limit.
  cpu: Optional[Union[float, tuple[float, float]]] = None,
  # Specify, in MiB, a memory request which is the minimum memory required.
  # Or, pass (request, limit) to additionally specify a hard limit in MiB.
  memory: Optional[Union[int, tuple[int, int]]] = None,
  block_network: bool = False, # Whether to block network access
  # List of CIDRs the sandbox is allowed to access. If None, all CIDRs are allowed.
  cidr_allowlist: Optional[Sequence[str]] = None,
  volumes: dict[
    Union[str, os.PathLike], Union[_Volume, _CloudBucketMount]
  ] = {}, # Mount points for Modal Volumes and CloudBucketMounts
  pty_info: Optional[api_pb2.PTYInfo] = None,
  # List of ports to tunnel into the sandbox. Encrypted ports are tunneled with TLS.
  encrypted_ports: Sequence[int] = [],
  # List of ports to tunnel into the sandbox without encryption.
  unencrypted_ports: Sequence[int] = [],
  # Reference to a Modal Proxy to use in front of this Sandbox.
  proxy: Optional[_Proxy] = None,
  # Enable memory snapshots.
  _experimental_enable_snapshot: bool = False,
  _experimental_scheduler_placement: Optional[
    SchedulerPlacement
  ] = None, # Experimental controls over fine-grained scheduling (alpha).
  client: Optional[_Client] = None,
) -> "_Sandbox":
```
 ## from_id
```
@staticmethod
def from_id(sandbox_id: str, client: Optional[_Client] = None) -> "_Sandbox":
```
 Construct a Sandbox from an id and look up the Sandbox result.
The ID of a Sandbox object can be accessed using `.object_id`.
## set_tags <a id="settags"></a>
```
def set_tags(self, tags: dict[str, str], *, client: Optional[_Client] = None):
```
 Set tags (key-value pairs) on the Sandbox. Tags can be used to filter results in `Sandbox.list`.
## snapshot_filesystem <a id="snapshotfilesystem"></a>
```
def snapshot_filesystem(self, timeout: int = 55) -> _Image:
```
 Snapshot the filesystem of the Sandbox.
Returns an `Image` (https://modal.com/docs/reference/modal.Image) object which can be used to spawn a new Sandbox with the same filesystem.
## wait <a id="wait"></a>
```
def wait(self, raise_on_termination: bool = True):
```
 Wait for the Sandbox to finish running.
## tunnels <a id="tunnels"></a>
```
def tunnels(self, timeout: int = 50) -> dict[int, Tunnel]:
```
 Get tunnel metadata for the sandbox.
Raises `SandboxTimeoutError` if the tunnels are not available after the timeout.
Returns a dictionary of `Tunnel` objects which are keyed by the container port.
NOTE: Previous to client v0.64.152, this returned a list of `TunnelData` objects.
## terminate <a id="terminate"></a>
```
def terminate(self):
```
 Terminate Sandbox execution.
This is a no-op if the Sandbox has already finished running.
## poll <a id="poll"></a>
```
def __init__(self, *args, **kwargs):
```
0 Check if the Sandbox has finished running.
Returns `None` if the Sandbox is still running, else returns the exit code.
## exec <a id="exec"></a>
```
def __init__(self, *args, **kwargs):
```
1 Execute a command in the Sandbox and return a ContainerProcess handle.
See the `ContainerProcess` (https://modal.com/docs/reference/modal.container_process# modalcontainer_processcontainerprocess) docs for more information.
* *Usage**
```
def __init__(self, *args, **kwargs):
```
2 ## open
```
def __init__(self, *args, **kwargs):
```
3 Open a file in the Sandbox and return a FileIO handle.
See the `FileIO` (https://modal.com/docs/reference/modal.file_io# modalfile_iofileio) docs for more information.
* *Usage**
```
def __init__(self, *args, **kwargs):
```
4 ## ls
```
def __init__(self, *args, **kwargs):
```
5 List the contents of a directory in the Sandbox.
## mkdir <a id="mkdir"></a>
```
def __init__(self, *args, **kwargs):
```
6 Create a new directory in the Sandbox.
## rm <a id="rm"></a>
```
def __init__(self, *args, **kwargs):
```
7 Remove a file or directory in the Sandbox.
## watch <a id="watch"></a>
```
def __init__(self, *args, **kwargs):
```
8 ## stdout
```
def __init__(self, *args, **kwargs):
```
9 `StreamReader` (https://modal.com/docs/reference/modal.io_streams# modalio_streamsstreamreader) for the sandboxs stdout stream.
## stderr <a id="stderr"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
0 `StreamReader` (https://modal.com/docs/reference/modal.io_streams# modalio_streamsstreamreader) for the sandboxs stderr stream.
## stdin <a id="stdin"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
1 `StreamWriter` (https://modal.com/docs/reference/modal.io_streams# modalio_streamsstreamwriter) for the sandboxs stdin stream.
## returncode <a id="returncode"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
2 Return code of the sandbox process if it has finished running, else `None`.
## list <a id="list"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
3 List all sandboxes for the current environment or app ID (if specified). If tags are specified, only sandboxes that have at least those tags are returned. Returns an iterator over `Sandbox` objects.
modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox# modalsandbox)hydrate (https://modal.com/docs/reference/modal.Sandbox# hydrate)create (https://modal.com/docs/reference/modal.Sandbox# create)from_id (https://modal.com/docs/reference/modal.Sandbox# from_id)set_tags (https://modal.com/docs/reference/modal.Sandbox# set_tags)snapshot_filesystem (https://modal.com/docs/reference/modal.Sandbox# snapshot_filesystem)wait (https://modal.com/docs/reference/modal.Sandbox# wait)tunnels (https://modal.com/docs/reference/modal.Sandbox# tunnels)terminate (https://modal.com/docs/reference/modal.Sandbox# terminate)poll (https://modal.com/docs/reference/modal.Sandbox# poll)exec (https://modal.com/docs/reference/modal.Sandbox# exec)open (https://modal.com/docs/reference/modal.Sandbox# open)ls (https://modal.com/docs/reference/modal.Sandbox# ls)mkdir (https://modal.com/docs/reference/modal.Sandbox# mkdir)rm (https://modal.com/docs/reference/modal.Sandbox# rm)watch (https://modal.com/docs/reference/modal.Sandbox# watch)stdout (https://modal.com/docs/reference/modal.Sandbox# stdout)stderr (https://modal.com/docs/reference/modal.Sandbox# stderr)stdin (https://modal.com/docs/reference/modal.Sandbox# stdin)returncode (https://modal.com/docs/reference/modal.Sandbox# returncode)list (https://modal.com/docs/reference/modal.Sandbox# list)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)