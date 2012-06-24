'''
Utilities shared by dxpy modules.
'''

import collections, concurrent.futures

def response_iterator(request_iterator, worker_pool, max_active_tasks=4):
    '''
    :param request_iterator: This is expected to be an iterator producing inputs for consumption by the worker pool.
    :param worker_pool: Assumed to be a concurrent.futures.Executor instance.
    :max_active_tasks: The maximum number of tasks that may be either running or waiting for consumption of their result.

    Rate-limited asynchronous multithreaded task runner.
    Consumes tasks from *request_iterator*. Yields them in order, while allowing up to *max_active_tasks* to run
    simultaneously. Unlike concurrent.futures.Executor.map, prevents new tasks from starting while there are
    *max_active_tasks* or more unconsumed results.
    '''
    future_deque = collections.deque()
    for i in range(max_active_tasks):
        try:
            f = worker_pool.submit(*request_iterator.next())
            future_deque.append(f)
        except StopIteration:
            break

    while len(future_deque) > 0:
        f = future_deque.popleft()
        if not f.done():
            concurrent.futures.wait([f])
        if f.exception() is not None:
            raise f.exception()
        try:
            next_future = worker_pool.submit(*request_iterator.next())
            future_deque.append(next_future)
        except StopIteration:
            pass
        yield f.result()
