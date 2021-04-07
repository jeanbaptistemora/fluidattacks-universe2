---
id: writing-code-suggestions
title: Writing fast and concurrent code, even at architectural windward
sidebar_label: Writing fast and concurrent code, even at architectural windward
slug: /devs/integrates/writing-code-suggestions
---

As you may have noticed, Integrates has async definitions in the top-level resolvers
of the GraphQL API. What this means is that you can use async/await keywords in all
downstream components.

This is, however, catchy because:
- Writing async/await statements do not make your code faster
- Writing async/await statements do not make your code concurrent

This has to be done intelligently taking into account the concepts and using high-level
language features that I'll explain below.

## **The current architecture**

There are N **main** event loops, each one is a separate thread that listens to incoming requests
and dispatch responses into M **secondary** event loops (let's call them **executor pools**
because that's what they are).

At the end of the day just develop as if there was only 1 main event loop that can
(optionally) dispatch tasks into the executor pools (secondary event loops), N is a multiplier
that allows us to scale horizontally by adding nodes to the cluster, and processes into the
ASGI depending on the resources of every instance

## **Blocking tasks**

Everything you are used to, code runs sequentially, and do not let the main event loop do other
things in the mean time:

```py
import time
from tracers.function import trace

@trace
def main():
  time.sleep(1)
  time.sleep(1)
  time.sleep(1)

main()

#
# 🛈  Finished transaction: 49a6bca8e60f433ab29376b19e643026, 3.00 seconds
#
#   #    Timestamp      %     Total    Nested Call Chain
#
#      1     0.00s 100.0%     3.00s    ✓ main()
#
```
It runs a, b, c, the event loop is busy in every sleep, total execution time: 3 seconds.

Another example:
```py
import asyncio
from tracers.function import trace

@trace
async def main():
  await asyncio.sleep(1)
  await asyncio.sleep(1)
  await asyncio.sleep(1)

asyncio.run(main())

#
# 🛈  Finished transaction: 638654ed6a7d414ebc52e9441b6e7c89, 3.00 seconds
#
#   #    Timestamp      %     Total    Nested Call Chain
#
#      1     0.00s 100.0%     3.00s    ✓ async main()
#
```
It runs a, b, c, the event loop is busy in every sleep, total execution time: 3 seconds.

**Yes, async/await stuff do not make your code faster out-of-the-box, nor asynchronous, nor concurrent.**

Being busy (blocked) means the event loop cannot run anything else in the meantime (blocked),
which is a synonym for your main event loop (which runs everybody's requests at Integrates)
not being able to handle incoming requests from other people (it's blocked!) which means
performance bottlenecks.

## **Blocking code examples**

Boto3 is blocking, which means all our current access to the database is blocking
(it's not asynchronous)

Almost all libraries that we currently use as well as all `def example()` functions are blocking,
only asyncio, and httpx libraries are asynchronous, there is probably an asynchronous version
of the thing you need so far but we've not migrated our code.
(We are not using aioboto3 right now for example).

Unless explicitly stated in the library documentation, python code is synchronous (blocking)

The way to avoid blocking the main event loop is to dispatch it into the executor pools with
`sync_to_async`. These executor pools may get blocked too and work in FIFO mode when they are
blocked, but at least allow the main event loop to listen for other requests meanwhile.
So they are not the solution, but they are better than nothing.

Example:

```py
from asgiref.sync import sync_to_async

async def _do_remove_evidence(...):
    success = await \
        sync_to_async(finding_domain.remove_evidence)(evidence_id, finding_id)

    return success
```

## **Coroutines**

When you call an `async def function` it returns a coroutine.
This is an object that can be awaited (`result = await function(...)`),
awaited coroutines are non-blocking (yay!) **BUT THEY ARE SERIAL** (non-concurrent)
(insert here translations.text_sad) which means they are the same thing we are used to
(slow serial classic code)

## **Tasks**

This is where your code starts getting faster, a task is kind of a future, it's being
materialized in the background and it's finally materialized when you **await** it:

```py
import asyncio
from tracers.function import trace

@trace
async def sleep(time: int):
    print(f'sleeping for: {time}')
    await asyncio.sleep(time)

@trace
async def main():
    result1 = asyncio.create_task(sleep(1))
    result2 = asyncio.create_task(sleep(1))
    result3 = asyncio.create_task(sleep(1))

    trace(print)('wtf, this is printed first, even though it is written after the sleeps')

    await result1
    await result2
    await result3

    trace(print)('this takes 1 second, even though we are sleeping for 3!!!')

asyncio.run(main())

# wtf, this is printed first, even though it is written after the sleeps
# sleeping for: 1
# sleeping for: 1
# sleeping for: 1
# this takes 1 second, even though we are sleeping for 3!!!
#
# 🛈  Finished transaction: f7188ffde77240568474fd88b5510303, 1.00 seconds
#
#   #    Timestamp      %     Total    Nested Call Chain
#
#      1     0.00s 100.0%     1.00s    ✓ async main()
#      2     0.00s   0.0%     0.00s    ¦   ✓ builtins.print(...)
#      3     0.00s   0.0%     0.00s    ¦   ✓ async sleep(time: int)
#      4     0.00s   0.0%     0.00s    ¦   ✓ async sleep(time: int)
#      5     0.00s  99.9%     1.00s    ¦   ✓ async sleep(time: int)
#      6     1.00s   0.0%     0.00s    ¦   ✓ builtins.print(...)
#
```

Yes, this means `asyncio.create_task` allows us to write **really asynchronous code**.
Code that can be run in the background, as long as it's non-blocking.

## **Unleashing concurrency**

Mix `asyncio.create_task` with `asyncio.gather` and your code will be concurrent:

Dummy example:

```py
import asyncio
from tracers.function import trace

@trace
async def load_finding(finding_id: str):
    print(f'loading finding, this operation takes: 1 second')
    await asyncio.sleep(1)
    return finding_id

@trace
async def main():
    tasks = [
        asyncio.create_task(load_finding(1))
        for finding in ['a', 'b', 'c']
    ]

    trace(print)('wtf, this is printed first, even though it is written after the heavy stuff')

    findings = await asyncio.gather(*tasks)

    trace(print)('this takes 1 second, even though we are loading 3 findings, each one takes 1 second!!!')

    trace(print)(findings)

asyncio.run(main())
```

Real life example:

```diff
--- a/django-apps/integrates-back-async/backend/api/resolvers/project.py
+++ b/django-apps/integrates-back-async/backend/api/resolvers/project.py
@@ -766,6 +766,10 @@ async def _get_alive_projects(info, filters) -> List[ProjectType]:
     selection_set.selections = req_fields
-    projects = [
-        await resolve(info, project, selection_set=selection_set)
+
+    projects = await asyncio.gather(*[
+        asyncio.create_task(
+            resolve(info, project, selection_set=selection_set)
+        )
         for project in alive_projects
-    ]
+    ])
+
     return await util.get_filtered_elements(projects, filters)
```

Assuming every downstream call is non-blocking, (or it has been wrapped with synced_to_async),
then every project is going to be loaded at the same time (**concurrency!!**), which means a
performance improvement of `initial_time/N`, where `N` is the number of groups to load, and
`initial_time` the time it used to take before unleashing concurrency.

Please read https://docs.python.org/3/library/asyncio-task.html for the greater good

Good bye!
