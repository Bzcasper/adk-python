---
title: "Modal.Dict"
url: "https://modal.com/docs/reference/modal.Dict"
date: "2025-04-15 01:06:34"
word_count: 1312
---

# Modal.Dict

**Source:** [https://modal.com/docs/reference/modal.Dict](https://modal.com/docs/reference/modal.Dict)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1312

## Table of Contents

- [modal.Dict](#modaldict)
  - [hydrate](#hydrate)
  - [ephemeral](#ephemeral)
  - [get](#get)
  - [contains](#contains)
  - [len](#len)
  - [update](#update)
  - [put](#put)
  - [pop](#pop)
  - [keys](#keys)
  - [values](#values)
  - [items](#items)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Dict <a id="modaldict"></a>
```
class Dict(modal.object.Object)
```
 Distributed dictionary for storage in Modal apps.
Dict contents can be essentially any object so long as they can be serialized by `cloudpickle`. This includes other Modal objects. If writing and reading in different environments (eg., writing locally and reading remotely), its necessary to have the library defining the data type installed, with compatible versions, on both sides. Additionally, cloudpickle serialization is not guaranteed to be deterministic, so it is generally recommended to use primitive types for keys.
* *Lifetime of a Dict and its items**
An individual dict entry will expire 30 days after it was last added to its Dict object. Additionally, data are stored in memory on the Modal server and could be lost due to unexpected server restarts. Because of this, `Dict` is best suited for storing short-term state and is not recommended for durable storage.
* *Usage**
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
 The `Dict` class offers a few methods for operations that are usually accomplished in Python with operators, such as `Dict.put` and `Dict.contains`. The advantage of these methods is that they can be safely called in an asynchronous context by using the `.aio` suffix on the method, whereas their operator-based analogues will always run synchronously and block the event loop.
For more examples, see the guide (https://modal.com/docs/guide/dicts-and-queues# modal-dicts).
## hydrate <a id="hydrate"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
 Synchronize the local object with its identity on the Modal server.
It is rarely necessary to call this method explicitly, as most operations will lazily hydrate when needed. The main use case is when you need to access object metadata, such as its ID.
_Added in v0.72.39_ : This method replaces the deprecated `.resolve()` method.
## ephemeral <a id="ephemeral"></a>
```
@classmethod
@contextmanager
def ephemeral(
  cls: type["_Dict"],
  data: Optional[dict] = None,
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  _heartbeat_sleep: float = EPHEMERAL_OBJECT_HEARTBEAT_SLEEP,
) -> Iterator["_Dict"]:
```
 Creates a new ephemeral dict within a context manager:
Usage:
```
from modal import Dict
with Dict.ephemeral() as d:
  d["foo"] = "bar"
```
```
async with Dict.ephemeral() as d:
  await d.put.aio("foo", "bar")
```
 ## from_name
```
@staticmethod
@renamed_parameter((2024, 12, 18), "label", "name")
def from_name(
  name: str,
  data: Optional[dict] = None,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  environment_name: Optional[str] = None,
  create_if_missing: bool = False,
) -> "_Dict":
```
 Reference a named Dict, creating if necessary.
In contrast to `modal.Dict.lookup`, this is a lazy method that defers hydrating the local object with metadata from Modal servers until the first time it is actually used.
```
d = modal.Dict.from_name("my-dict", create_if_missing=True)
d[123] = 456
```
 ## lookup
```
@staticmethod
@renamed_parameter((2024, 12, 18), "label", "name")
def lookup(
  name: str,
  data: Optional[dict] = None,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  create_if_missing: bool = False,
) -> "_Dict":
```
 Lookup a named Dict.
DEPRECATED: This method is deprecated in favor of `modal.Dict.from_name`.
In contrast to `modal.Dict.from_name`, this is an eager method that will hydrate the local object with metadata from Modal servers.
```
d = modal.Dict.from_name("my-dict")
d["xyz"] = 123
```
 ## delete
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
0 ## clear
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
1 Remove all items from the Dict.
## get <a id="get"></a>
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
2 Get the value associated with a key.
Returns `default` if key does not exist.
## contains <a id="contains"></a>
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
3 Return if a key is present.
## len <a id="len"></a>
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
4 Return the length of the dictionary, including any expired keys.
## update <a id="update"></a>
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
5 Update the dictionary with additional items.
## put <a id="put"></a>
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
6 Add a specific key-value pair to the dictionary.
## pop <a id="pop"></a>
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
7 Remove a key from the dictionary, returning the value if it exists.
## keys <a id="keys"></a>
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
8 Return an iterator over the keys in this dictionary.
Note that (unlike with Python dicts) the return value is a simple iterator, and results are unordered.
## values <a id="values"></a>
```
from modal import Dict
my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)
my_dict["some key"] = "some value"
my_dict[123] = 456
assert my_dict["some key"] == "some value"
assert my_dict[123] == 456
```
9 Return an iterator over the values in this dictionary.
Note that (unlike with Python dicts) the return value is a simple iterator, and results are unordered.
## items <a id="items"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
0 Return an iterator over the (key, value) tuples in this dictionary.
Note that (unlike with Python dicts) the return value is a simple iterator, and results are unordered.
modal.Dict (https://modal.com/docs/reference/modal.Dict# modaldict)hydrate (https://modal.com/docs/reference/modal.Dict# hydrate)ephemeral (https://modal.com/docs/reference/modal.Dict# ephemeral)from_name (https://modal.com/docs/reference/modal.Dict# from_name)lookup (https://modal.com/docs/reference/modal.Dict# lookup)delete (https://modal.com/docs/reference/modal.Dict# delete)clear (https://modal.com/docs/reference/modal.Dict# clear)get (https://modal.com/docs/reference/modal.Dict# get)contains (https://modal.com/docs/reference/modal.Dict# contains)len (https://modal.com/docs/reference/modal.Dict# len)update (https://modal.com/docs/reference/modal.Dict# update)put (https://modal.com/docs/reference/modal.Dict# put)pop (https://modal.com/docs/reference/modal.Dict# pop)keys (https://modal.com/docs/reference/modal.Dict# keys)values (https://modal.com/docs/reference/modal.Dict# values)items (https://modal.com/docs/reference/modal.Dict# items)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)