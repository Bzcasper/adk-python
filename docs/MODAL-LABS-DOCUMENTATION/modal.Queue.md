---
title: "Modal.Queue"
url: "https://modal.com/docs/reference/modal.Queue"
date: "2025-04-15 01:06:34"
word_count: 1535
---

# Modal.Queue

**Source:** [https://modal.com/docs/reference/modal.Queue](https://modal.com/docs/reference/modal.Queue)  
**Crawled:** 2025-04-15 01:06:34  
**Word Count:** 1535

## Table of Contents

- [modal.Queue](#modalqueue)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
  - [hydrate](#hydrate)
  - [validate_partition_key](#validatepartitionkey)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
  - [get](#get)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
  - [get_many](#getmany)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
  - [put](#put)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
  - [put_many](#putmany)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
  - [len](#len)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)
  - [iterate](#iterate)
- [Create an ephemeral queue which is anonymous and garbage collected](#create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected)
- [You can also create persistent queues that can be used across apps](#you-can-also-create-persistent-queues-that-can-be-used-across-apps)

---

![Modal logo (https://modal.com/_app/immutable/assets/logotype-docs._cZdhNtZ.svg)](https://modal.com/docs)
Guide (https://modal.com/docs/guide)Examples (https://modal.com/docs/examples)Reference (https://modal.com/docs/reference)Playground (https://modal.com/playground)
Search`K`
Log In (https://modal.com/login?next=%2Fapps) Sign Up (https://modal.com/signup?next=%2Fapps)
Changelog (https://modal.com/docs/reference/changelog) API Reference (https://modal.com/docs/reference/modal.App) modal.App (https://modal.com/docs/reference/modal.App)modal.Client (https://modal.com/docs/reference/modal.Client)modal.CloudBucketMount (https://modal.com/docs/reference/modal.CloudBucketMount)modal.Cls (https://modal.com/docs/reference/modal.Cls)modal.Cron (https://modal.com/docs/reference/modal.Cron)modal.Dict (https://modal.com/docs/reference/modal.Dict)modal.Error (https://modal.com/docs/reference/modal.Error)modal.FilePatternMatcher (https://modal.com/docs/reference/modal.FilePatternMatcher)modal.Function (https://modal.com/docs/reference/modal.Function)modal.FunctionCall (https://modal.com/docs/reference/modal.FunctionCall)modal.Image (https://modal.com/docs/reference/modal.Image)modal.Mount (https://modal.com/docs/reference/modal.Mount)modal.NetworkFileSystem (https://modal.com/docs/reference/modal.NetworkFileSystem)modal.Period (https://modal.com/docs/reference/modal.Period)modal.Proxy (https://modal.com/docs/reference/modal.Proxy)modal.Queue (https://modal.com/docs/reference/modal.Queue)modal.Retries (https://modal.com/docs/reference/modal.Retries)modal.Sandbox (https://modal.com/docs/reference/modal.Sandbox)modal.SandboxSnapshot (https://modal.com/docs/reference/modal.SandboxSnapshot)modal.Secret (https://modal.com/docs/reference/modal.Secret)modal.Tunnel (https://modal.com/docs/reference/modal.Tunnel)modal.Volume (https://modal.com/docs/reference/modal.Volume)modal.asgi_app (https://modal.com/docs/reference/modal.asgi_app)modal.batched (https://modal.com/docs/reference/modal.batched)modal.build (https://modal.com/docs/reference/modal.build)modal.call_graph (https://modal.com/docs/reference/modal.call_graph)modal.concurrent (https://modal.com/docs/reference/modal.concurrent)modal.container_process (https://modal.com/docs/reference/modal.container_process)modal.current_function_call_id (https://modal.com/docs/reference/modal.current_function_call_id)modal.current_input_id (https://modal.com/docs/reference/modal.current_input_id)modal.enable_output (https://modal.com/docs/reference/modal.enable_output)modal.enter (https://modal.com/docs/reference/modal.enter)modal.exit (https://modal.com/docs/reference/modal.exit)modal.fastapi_endpoint (https://modal.com/docs/reference/modal.fastapi_endpoint)modal.file_io (https://modal.com/docs/reference/modal.file_io)modal.forward (https://modal.com/docs/reference/modal.forward)modal.gpu (https://modal.com/docs/reference/modal.gpu)modal.interact (https://modal.com/docs/reference/modal.interact)modal.io_streams (https://modal.com/docs/reference/modal.io_streams)modal.is_local (https://modal.com/docs/reference/modal.is_local)modal.method (https://modal.com/docs/reference/modal.method)modal.parameter (https://modal.com/docs/reference/modal.parameter)modal.runner (https://modal.com/docs/reference/modal.runner)modal.web_endpoint (https://modal.com/docs/reference/modal.web_endpoint)modal.web_server (https://modal.com/docs/reference/modal.web_server)modal.wsgi_app (https://modal.com/docs/reference/modal.wsgi_app)modal.exception (https://modal.com/docs/reference/modal.exception)modal.config (https://modal.com/docs/reference/modal.config) CLI Reference (https://modal.com/docs/reference/cli/app) modal app (https://modal.com/docs/reference/cli/app)modal config (https://modal.com/docs/reference/cli/config)modal container (https://modal.com/docs/reference/cli/container)modal deploy (https://modal.com/docs/reference/cli/deploy)modal dict (https://modal.com/docs/reference/cli/dict)modal environment (https://modal.com/docs/reference/cli/environment)modal launch (https://modal.com/docs/reference/cli/launch)modal nfs (https://modal.com/docs/reference/cli/nfs)modal profile (https://modal.com/docs/reference/cli/profile)modal queue (https://modal.com/docs/reference/cli/queue)modal run (https://modal.com/docs/reference/cli/run)modal secret (https://modal.com/docs/reference/cli/secret)modal serve (https://modal.com/docs/reference/cli/serve)modal setup (https://modal.com/docs/reference/cli/setup)modal shell (https://modal.com/docs/reference/cli/shell)modal token (https://modal.com/docs/reference/cli/token)modal volume (https://modal.com/docs/reference/cli/volume)
# modal.Queue <a id="modalqueue"></a>
```
class Queue(modal.object.Object)
```
 Distributed, FIFO queue for data flow in Modal apps.
The queue can contain any object serializable by `cloudpickle`, including Modal objects.
By default, the `Queue` object acts as a single FIFO queue which supports puts and gets (blocking and non-blocking).
* *Usage**
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a> <a id="create-an-ephemeral-queue-which-is-anonymous-and-garbage-collected"></a>
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a> <a id="you-can-also-create-persistent-queues-that-can-be-used-across-apps"></a>
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
 For more examples, see the guide (https://modal.com/docs/guide/dicts-and-queues# modal-queues).
* *Queue partitions (beta)**
Specifying partition keys gives access to other independent FIFO partitions within the same `Queue` object. Across any two partitions, puts and gets are completely independent. For example, a put in one partition does not affect a get in any other partition.
When no partition key is specified (by default), puts and gets will operate on a default partition. This default partition is also isolated from all other partitions. Please see the Usage section below for an example using partitions.
* *Lifetime of a queue and its partitions**
By default, each partition is cleared 24 hours after the last `put` operation. A lower TTL can be specified by the `partition_ttl` argument in the `put` or `put_many` methods. Each partitions expiry is handled independently.
As such, `Queue`s are best used for communication between active functions and not relied on for persistent storage.
On app completion or after stopping an app any associated `Queue` objects are cleaned up. All its partitions will be cleared.
* *Limits**
A single `Queue` can contain up to 100,000 partitions, each with up to 5,000 items. Each item can be up to 1 MiB.
Partition keys must be non-empty and must not exceed 64 bytes.
## hydrate <a id="hydrate"></a>
```
def hydrate(self, client: Optional[_Client] = None) -> Self:
```
 Synchronize the local object with its identity on the Modal server.
It is rarely necessary to call this method explicitly, as most operations will lazily hydrate when needed. The main use case is when you need to access object metadata, such as its ID.
_Added in v0.72.39_ : This method replaces the deprecated `.resolve()` method.
## validate_partition_key <a id="validatepartitionkey"></a>
```
@staticmethod
def validate_partition_key(partition: Optional[str]) -> bytes:
```
 ## ephemeral
```
@classmethod
@contextmanager
def ephemeral(
  cls: type["_Queue"],
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  _heartbeat_sleep: float = EPHEMERAL_OBJECT_HEARTBEAT_SLEEP,
) -> Iterator["_Queue"]:
```
 Creates a new ephemeral queue within a context manager:
Usage:
```
from modal import Queue
with Queue.ephemeral() as q:
  q.put(123)
```
```
async with Queue.ephemeral() as q:
  await q.put.aio(123)
```
 ## from_name
```
@staticmethod
@renamed_parameter((2024, 12, 18), "label", "name")
def from_name(
  name: str,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  environment_name: Optional[str] = None,
  create_if_missing: bool = False,
) -> "_Queue":
```
 Reference a named Queue, creating if necessary.
In contrast to `modal.Queue.lookup`, this is a lazy method the defers hydrating the local object with metadata from Modal servers until the first time it is actually used.
```
q = modal.Queue.from_name("my-queue", create_if_missing=True)
q.put(123)
```
 ## lookup
```
@staticmethod
@renamed_parameter((2024, 12, 18), "label", "name")
def lookup(
  name: str,
  namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
  client: Optional[_Client] = None,
  environment_name: Optional[str] = None,
  create_if_missing: bool = False,
) -> "_Queue":
```
 Lookup a named Queue.
DEPRECATED: This method is deprecated in favor of `modal.Queue.from_name`.
In contrast to `modal.Queue.from_name`, this is an eager method that will hydrate the local object with metadata from Modal servers.
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
0 ## delete
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
1 ## clear
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
2 Clear the contents of a single partition or all partitions.
## get <a id="get"></a>
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
3 Remove and return the next object in the queue.
If `block` is `True` (the default) and the queue is empty, `get` will wait indefinitely for an object, or until `timeout` if specified. Raises a native `queue.Empty` exception if the `timeout` is reached.
If `block` is `False`, `get` returns `None` immediately if the queue is empty. The `timeout` is ignored in this case.
## get_many <a id="getmany"></a>
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
4 Remove and return up to `n_values` objects from the queue.
If there are fewer than `n_values` items in the queue, return all of them.
If `block` is `True` (the default) and the queue is empty, `get` will wait indefinitely for at least 1 object to be present, or until `timeout` if specified. Raises the stdlibs `queue.Empty` exception if the `timeout` is reached.
If `block` is `False`, `get` returns `None` immediately if the queue is empty. The `timeout` is ignored in this case.
## put <a id="put"></a>
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
5 Add an object to the end of the queue.
If `block` is `True` and the queue is full, this method will retry indefinitely or until `timeout` if specified. Raises the stdlibs `queue.Full` exception if the `timeout` is reached. If blocking it is not recommended to omit the `timeout`, as the operation could wait indefinitely.
If `block` is `False`, this method raises `queue.Full` immediately if the queue is full. The `timeout` is ignored in this case.
## put_many <a id="putmany"></a>
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
6 Add several objects to the end of the queue.
If `block` is `True` and the queue is full, this method will retry indefinitely or until `timeout` if specified. Raises the stdlibs `queue.Full` exception if the `timeout` is reached. If blocking it is not recommended to omit the `timeout`, as the operation could wait indefinitely.
If `block` is `False`, this method raises `queue.Full` immediately if the queue is full. The `timeout` is ignored in this case.
## len <a id="len"></a>
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
7 Return the number of objects in the queue partition.
## iterate <a id="iterate"></a>
```
from modal import Queue
# Create an ephemeral queue which is anonymous and garbage collected
with Queue.ephemeral() as my_queue:
  # Putting values
  my_queue.put("some value")
  my_queue.put(123)
  # Getting values
  assert my_queue.get() == "some value"
  assert my_queue.get() == 123
  # Using partitions
  my_queue.put(0)
  my_queue.put(1, partition="foo")
  my_queue.put(2, partition="bar")
  # Default and "foo" partition are ignored by the get operation.
  assert my_queue.get(partition="bar") == 2
  # Set custom 10s expiration time on "foo" partition.
  my_queue.put(3, partition="foo", partition_ttl=10)
  # (beta feature) Iterate through items in place (read immutably)
  my_queue.put(1)
  assert [v for v in my_queue.iterate()] == [0, 1]
# You can also create persistent queues that can be used across apps
queue = Queue.from_name("my-persisted-queue", create_if_missing=True)
queue.put(42)
assert queue.get() == 42
```
8 (Beta feature) Iterate through items in the queue without mutation.
Specify `item_poll_timeout` to control how long the iterator should wait for the next time before giving up.
modal.Queue (https://modal.com/docs/reference/modal.Queue# modalqueue)hydrate (https://modal.com/docs/reference/modal.Queue# hydrate)validate_partition_key (https://modal.com/docs/reference/modal.Queue# validate_partition_key)ephemeral (https://modal.com/docs/reference/modal.Queue# ephemeral)from_name (https://modal.com/docs/reference/modal.Queue# from_name)lookup (https://modal.com/docs/reference/modal.Queue# lookup)delete (https://modal.com/docs/reference/modal.Queue# delete)clear (https://modal.com/docs/reference/modal.Queue# clear)get (https://modal.com/docs/reference/modal.Queue# get)get_many (https://modal.com/docs/reference/modal.Queue# get_many)put (https://modal.com/docs/reference/modal.Queue# put)put_many (https://modal.com/docs/reference/modal.Queue# put_many)len (https://modal.com/docs/reference/modal.Queue# len)iterate (https://modal.com/docs/reference/modal.Queue# iterate)
!Modal logo (https://modal.com/_app/immutable/assets/logotype.CAx-nu9G.svg)  2025
About (https://modal.com/company) Status (https://status.modal.com/) Changelog (https://modal.com/docs/reference/changelog) Documentation (https://modal.com/docs/guide) Slack Community (https://modal.com/slack) Pricing (https://modal.com/pricing) Examples (https://modal.com/docs/examples)