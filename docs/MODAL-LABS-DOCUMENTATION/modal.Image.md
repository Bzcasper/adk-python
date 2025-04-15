---
title: "Modal.Image"
url: "https://modal.com/docs/reference/modal.Image"
date: "2025-04-15 01:06:34"
word_count: 2391
---

# Modal.Image

**Source:** [https://modal.com/docs/reference/modal.Image](https://modal.com/docs/reference/modal.Image)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 2391

## Table of Contents

- [modal.Image](#modalimage)
  - [copy_mount](#copymount)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
  - [add_local_dir](#addlocaldir)
- [When including files is simpler than excluding them, you can use the `~` operator to invert the matcher.](#when-including-files-is-simpler-than-excluding-them-you-can-use-the--operator-to-invert-the-matcher)
- [You can also read ignore patterns from a file.](#you-can-also-read-ignore-patterns-from-a-file)
  - [copy_local_file](#copylocalfile)
  - [add_local_python_source](#addlocalpythonsource)
  - [copy_local_dir](#copylocaldir)
  - [pip_install](#pipinstall)
  - [pip_install_from_pyproject](#pipinstallfrompyproject)
  - [poetry_install_from_file](#poetryinstallfromfile)
  - [dockerfile_commands](#dockerfilecommands)
  - [shell](#shell)
  - [run_commands](#runcommands)
  - [micromamba](#micromamba)
  - [micromamba_install](#micromambainstall)
  - [from_registry](#fromregistry)
  - [apt_install](#aptinstall)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)
- [place all static images in root of mount](#place-all-static-images-in-root-of-mount)
- [place mount's contents into /static directory of image.](#place-mounts-contents-into-static-directory-of-image)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Image <a id="modalimage"></a>
```
class Image(modal.object.Object)
```
 Base class for container images to run functions in.
Do not construct this class directly; instead use one of its static factory methods, such as `modal.Image.debian_slim`, `modal.Image.from_registry`, or `modal.Image.micromamba`.
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
## copy_mount <a id="copymount"></a>
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
 * *Deprecated** : Use image.add_local_dir(, =True) or similar instead. the entire contents of a `modal.Mount` into an image. Useful when files only available locally are required during the image build process.
* *Example**
```
static_images_dir = "./static"
# place all static images in root of mount <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a> <a id="place-all-static-images-in-root-of-mount"></a>
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image. <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a> <a id="place-mounts-contents-into-static-directory-of-image"></a>
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
 ## add_local_file
```
def add_local_file(self, local_path: Union[str, Path], remote_path: str, *, : bool = False) -> "_Image":
```
 Adds a local file to the image at `remote_path` within the container
By default (`=False`), the files are added to containers on startup and are not built into the actual Image, which speeds up deployment.
Set `=True` to the files into an Image layer at build time instead, similar to how works in a `Dockerfile`.
=True can slow down iteration since it requires a rebuild of the Image and any subsequent build steps whenever the included files change, but it is required if you want to run additional build steps after this one.
_Added in v0.66.40_ : This method replaces the deprecated `modal.Image.copy_local_file` method.
## add_local_dir <a id="addlocaldir"></a>
```
def add_local_dir(
  self,
  local_path: Union[str, Path],
  remote_path: str,
  *,
  : bool = False,
  # Predicate filter function for file exclusion, which should accept a filepath and return `True` for exclusion.
  # Defaults to excluding no files. If a Sequence is provided, it will be converted to a FilePatternMatcher.
  # Which follows dockerignore syntax.
  ignore: Union[Sequence[str], Callable[[Path], bool]] = [],
) -> "_Image":
```
 Adds a local directorys content to the image at `remote_path` within the container
By default (`=False`), the files are added to containers on startup and are not built into the actual Image, which speeds up deployment.
Set `=True` to the files into an Image layer at build time instead, similar to how works in a `Dockerfile`.
=True can slow down iteration since it requires a rebuild of the Image and any subsequent build steps whenever the included files change, but it is required if you want to run additional build steps after this one.
* *Usage:**
```
from modal import FilePatternMatcher
image = modal.Image.debian_slim().add_local_dir(
  "~/assets",
  remote_path="/assets",
  ignore=["*.venv"],
)
image = modal.Image.debian_slim().add_local_dir(
  "~/assets",
  remote_path="/assets",
  ignore=lambda p: p.is_relative_to(".venv"),
)
image = modal.Image.debian_slim().add_local_dir(
  "~/assets",
  remote_path="/assets",
  ignore=FilePatternMatcher("**/*.txt"),
)
# When including files is simpler than excluding them, you can use the `~` operator to invert the matcher. <a id="when-including-files-is-simpler-than-excluding-them-you-can-use-the--operator-to-invert-the-matcher"></a>
image = modal.Image.debian_slim().add_local_dir(
  "~/assets",
  remote_path="/assets",
  ignore=~FilePatternMatcher("**/*.py"),
)
# You can also read ignore patterns from a file. <a id="you-can-also-read-ignore-patterns-from-a-file"></a>
image = modal.Image.debian_slim().add_local_dir(
  "~/assets",
  remote_path="/assets",
  ignore=FilePatternMatcher.from_file("/path/to/ignorefile"),
)
```
 _Added in v0.66.40_ : This method replaces the deprecated `modal.Image.copy_local_dir` method.
## copy_local_file <a id="copylocalfile"></a>
```
def copy_local_file(self, local_path: Union[str, Path], remote_path: Union[str, Path] = "./") -> "_Image":
```
 a file into the image as a part of building it.
This works in a similar way to works in a `Dockerfile`.
## add_local_python_source <a id="addlocalpythonsource"></a>
```
def add_local_python_source(
  self, *modules: str, : bool = False, ignore: Union[Sequence[str], Callable[[Path], bool]] = NON_PYTHON_FILES
) -> "_Image":
```
 Adds locally available Python packages/modules to containers
Adds all files from the specified Python package or module to containers running the Image.
Packages are added to the `/root` directory of containers, which is on the `PYTHONPATH` of any executed Modal Functions, enabling import of the module by that name.
By default (`=False`), the files are added to containers on startup and are not built into the actual Image, which speeds up deployment.
Set `=True` to the files into an Image layer at build time instead. This can slow down iteration since it requires a rebuild of the Image and any subsequent build steps whenever the included files change, but it is required if you want to run additional build steps after this one.
* *Note:** This excludes all dot-prefixed subdirectories or files and all `.pyc`/`__pycache__` files. To add full directories with finer control, use `.add_local_dir()` instead and specify `/root` as the destination directory.
By default only includes `.py`-files in the source modules. Set the `ignore` argument to a list of patterns or a callable to override this behavior, e.g.:
```
def __init__(self, *args, **kwargs):
```
0 _Added in v0.67.28_ : This method replaces the deprecated `modal.Mount.from_local_python_packages` pattern.
## copy_local_dir <a id="copylocaldir"></a>
```
def __init__(self, *args, **kwargs):
```
1 * *Deprecated** : Use image.add_local_dir instead a directory into the image as a part of building the image.
This works in a similar way to works in a `Dockerfile`.
* *Usage:**
```
def __init__(self, *args, **kwargs):
```
2 ## from_id
```
def __init__(self, *args, **kwargs):
```
3 Construct an Image from an id and look up the Image result.
The ID of an Image object can be accessed using `.object_id`.
## pip_install <a id="pipinstall"></a>
```
def __init__(self, *args, **kwargs):
```
4 Install a list of Python packages using pip.
* *Examples**
Simple installation:
```
def __init__(self, *args, **kwargs):
```
5 More complex installation:
```
def __init__(self, *args, **kwargs):
```
6 ## pip_install_private_repos
```
def __init__(self, *args, **kwargs):
```
7 Install a list of Python packages from private git repositories using pip.
This method currently supports Github and Gitlab only. * **Github:** Provide a `modal.Secret` that contains a `GITHUB_TOKEN` key-value pair * **Gitlab:** Provide a `modal.Secret` that contains a `GITLAB_TOKEN` key-value pair These API tokens should have permissions to read the list of private repositories provided as arguments.
We recommend using Githubs . These tokens are repo-scoped, and avoid granting read permission across all of a users private repos.
* *Example**
```
def __init__(self, *args, **kwargs):
```
8 ## pip_install_from_requirements
```
def __init__(self, *args, **kwargs):
```
9 Install a list of Python packages from a local `requirements.txt` file.
## pip_install_from_pyproject <a id="pipinstallfrompyproject"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
0 Install dependencies specified by a local `pyproject.toml` file.
`optional_dependencies` is a list of the keys of the optional-dependencies section(s) of the `pyproject.toml` file (e.g. test, doc, experiment, etc). When provided, all of the packages in each listed section are installed as well.
## poetry_install_from_file <a id="poetryinstallfromfile"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
1 Install poetry _dependencies_ specified by a local `pyproject.toml` file.
If not provided as argument the path to the lockfile is inferred. However, the file has to exist, unless `ignore_lockfile` is set to `True`.
Note that the root project of the poetry project is not installed, only the dependencies. For including local python source files see `add_local_python_source`
## dockerfile_commands <a id="dockerfilecommands"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
2 Extend an image with arbitrary Dockerfile-like commands.
* *Usage:**
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
3 ## entrypoint
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
4 Set the entrypoint for the image.
## shell <a id="shell"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
5 Overwrite default shell for the image.
## run_commands <a id="runcommands"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
6 Extend an image with a list of shell commands to run.
## micromamba <a id="micromamba"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
7 A Micromamba base image. Micromamba allows for fast building of small Conda-based containers.
## micromamba_install <a id="micromambainstall"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
8 Install a list of additional packages using micromamba.
## from_registry <a id="fromregistry"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
9 Build a Modal Image from a public or private image registry, such as Docker Hub.
The image must be built for the `linux/amd64` platform.
If your image does not come with Python installed, you can use the `add_python` parameter to specify a version of Python to add to the image. Otherwise, the image is expected to have Python on PATH as `python`, along with `pip`.
You may also use `setup_dockerfile_commands` to run Dockerfile commands before the remaining commands run. This might be useful if you want a custom Python installation or to set a `SHELL`. Prefer `run_commands()` when possible though.
To authenticate against a private registry with static credentials, you must set the `secret` parameter to a `modal.Secret` containing a username (`REGISTRY_USERNAME`) and an access token or password (`REGISTRY_PASSWORD`).
To authenticate against private registries with credentials from a cloud provider, use `Image.from_gcp_artifact_registry()` or `Image.from_aws_ecr()`.
* *Examples**
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
0 ## from_gcp_artifact_registry
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
1 Build a Modal image from a private image in Google Cloud Platform (GCP) Artifact Registry.
You will need to pass a `modal.Secret` containing as `SERVICE_ACCOUNT_JSON`. This can be done from the Secrets (https://modal.com/secrets) page. Your service account should be granted a specific role depending on the GCP registry used: * For Artifact Registry images (`pkg.dev` domains) use the role * For Container Registry images (`gcr.io` domains) use the role * *Note:** This method does not use `GOOGLE_APPLICATION_CREDENTIALS` as that variable accepts a path to a JSON file, not the actual JSON string.
See `Image.from_registry()` for information about the other parameters.
* *Example**
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
2 ## from_aws_ecr
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
3 Build a Modal image from a private image in AWS Elastic Container Registry (ECR).
You will need to pass a `modal.Secret` containing `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION` to access the target ECR registry.
IAM configuration details can be found in the AWS documentation for .
See `Image.from_registry()` for information about the other parameters.
* *Example**
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
4 ## from_dockerfile
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
5 Build a Modal image from a local Dockerfile.
If your Dockerfile does not have Python installed, you can use the `add_python` parameter to specify a version of Python to add to the image.
* *Usage:**
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
6 ## debian_slim
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
7 Default image, based on the official `python` Docker images.
## apt_install <a id="aptinstall"></a>
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
8 Install a list of Debian packages using `apt`.
* *Example**
```
def copy_mount(self, mount: _Mount, remote_path: Union[str, Path] = ".") -> "_Image":
```
9 ## run_function
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
0 Run user-defined function `raw_f` as an image build step. The function runs just like an ordinary Modal function, and any kwargs accepted by `@app.function` (such as `Mount`s, `NetworkFileSystem`s, and resource requests) can be supplied to it. After it finishes execution, a snapshot of the resulting container file system is saved as an image.
* *Note**
Only the source code of `raw_f`, the contents of `**kwargs`, and any referenced _global_ variables are used to determine whether the image has changed and needs to be rebuilt. If this function references other functions or variables, the image will not be rebuilt if you make changes to them. You can force a rebuild by changing the functions source code itself.
* *Example**
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
1 ## env
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
2 Sets the environment variables in an Image.
* *Example**
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
3 ## workdir
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
4 Set the working directory for subsequent image build steps and function execution.
* *Example**
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
5 ## cmd
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
6 Set the default entrypoint argument (`CMD`) for the image.
* *Example**
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
7 ## imports
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
8 Used to import packages in global scope that are only available when running remotely. By using this context manager you can avoid an `ImportError` due to not having certain packages installed locally.
* *Usage:**
```
static_images_dir = "./static"
# place all static images in root of mount
mount = modal.Mount.from_local_dir(static_images_dir, remote_path="/")
# place mount's contents into /static directory of image.
image = modal.Image.debian_slim().copy_mount(mount, remote_path="/static")
```
9 modal.Image (https://modal.com/docs/reference/modal.Image# modalimage)hydrate (https://modal.com/docs/reference/modal.Image# hydrate)copy_mount (https://modal.com/docs/reference/modal.Image# copy_mount)add_local_file (https://modal.com/docs/reference/modal.Image# add_local_file)add_local_dir (https://modal.com/docs/reference/modal.Image# add_local_dir)copy_local_file (https://modal.com/docs/reference/modal.Image# copy_local_file)add_local_python_source (https://modal.com/docs/reference/modal.Image# add_local_python_source)copy_local_dir (https://modal.com/docs/reference/modal.Image# copy_local_dir)from_id (https://modal.com/docs/reference/modal.Image# from_id)pip_install (https://modal.com/docs/reference/modal.Image# pip_install)pip_install_private_repos (https://modal.com/docs/reference/modal.Image# pip_install_private_repos)pip_install_from_requirements (https://modal.com/docs/reference/modal.Image# pip_install_from_requirements)pip_install_from_pyproject (https://modal.com/docs/reference/modal.Image# pip_install_from_pyproject)poetry_install_from_file (https://modal.com/docs/reference/modal.Image# poetry_install_from_file)dockerfile_commands (https://modal.com/docs/reference/modal.Image# dockerfile_commands)entrypoint (https://modal.com/docs/reference/modal.Image# entrypoint)shell (https://modal.com/docs/reference/modal.Image# shell)run_commands (https://modal.com/docs/reference/modal.Image# run_commands)micromamba (https://modal.com/docs/reference/modal.Image# micromamba)micromamba_install (https://modal.com/docs/reference/modal.Image# micromamba_install)from_registry (https://modal.com/docs/reference/modal.Image# from_registry)from_gcp_artifact_registry (https://modal.com/docs/reference/modal.Image# from_gcp_artifact_registry)from_aws_ecr (https://modal.com/docs/reference/modal.Image# from_aws_ecr)from_dockerfile (https://modal.com/docs/reference/modal.Image# from_dockerfile)debian_slim (https://modal.com/docs/reference/modal.Image# debian_slim)apt_install (https://modal.com/docs/reference/modal.Image# apt_install)run_function (https://modal.com/docs/reference/modal.Image# run_function)env (https://modal.com/docs/reference/modal.Image# env)workdir (https://modal.com/docs/reference/modal.Image# workdir)cmd (https://modal.com/docs/reference/modal.Image# cmd)imports (https://modal.com/docs/reference/modal.Image# imports)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)