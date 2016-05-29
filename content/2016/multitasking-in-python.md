Title: Multitasking in Python with multiprocessing
Slug: multitasking-in-python
Date: 2016-05-29 16:02
Tags: Python, Multiprocessing, Multithreading
Author: Laurens

I have been wanting to look at multiprocessing capabilities for some time now and I
 finally got around to it. Python is a great expressive language that is easy to
 code and easy to read. It really is my favourite language. One of the limits of
 Python is the lack of multithreading and/or multiprocessing. A Python process will
 always be running on a single. I suppose this made sense given in the days where
 computers with multiple processing cores were not as abundant as now. However, now
 a Python script can really seem to lack in speed simply because of this limitation.

I have come across multiple situations where I had wished that I access the extra
cores that I have available. Some of the math questions I like to solve at [Project
Euler](www.projecteuler.net) were rather computationally intensive and had
[emberassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel)
properties that could easily be exploited to improve performance. The same holds for
financial computations, where monte carlo simulations often appear that could
benefit from the same parallelisation. Being able to write parallel code really
could help me out.

# The Multiprocessing package
The solution to this can be find in the Standard Library of Python. The
*Multiprocessing* module provides us a lot of the tools that we need. First of all,
the Multiprocessing package is very similar to the Threading package. The difference
between multiprocessing and multithreading was confusing to me at first but is
actually quite simple. Multiprocesses spawns new Python processes. One should see
these as seperate Python instances that can run on another core and is thus able to
perform more calculations in the same amount of time. Since a completely new Python interpreter is launched, sharing objects and data is much harder.

Multithreading on the other hand does not launch a new Python instance. Instead it spawns threads that run in the same Python process. My first thought was that this is pretty useless as it does not really solve the problem of accessing more cores because it uses the same process that is bound to a single core. But don't be fooled, as threads simply serve an entirely different purpose. When your computations is mainly bound by the (lack of) speed of I/O operations, then threads really are all you need. When performing an I/O operation, Python blocks the complete process and waits for the operation to finish before it can continue (so called *synchronous* behaviour). If you need to do many of these operations and they are independent of eachother, then one would like to run several of these operations simultaneously. With threads, this is possible.

Now you might wonder, should I learn about two different packages depending on my specific needs? The answer is no. A need little trick about the multiprocessing package is that it can serve as a wrapper around the multithreading package. Simply instead of
```Python
from multiprocessing import Process
```
one can also use
```Python
from multiprocessing.dummy import Process
```
I thought this is quite neat.

## My example: multitasking with deamonic processes
For one of my projects, I wanted to be able to run several workers simultaneously. These workers would then each complete independent tasks indefinitely. That is, these worker processes would be [daemonic](https://en.wikipedia.org/wiki/Daemon_(computing)). Something that was specific to my need is that workers are not equals. Worker A would be doing very different tasks than worker B. And if any of the workers crash, their respective tasks will be left undone. Hence, it is essential that workers are restarted upon failure.

After some testing, the following script does exactly what I need:
```Python
from multiprocessing import Process
from time import sleep
import sys
from functools import wraps
from random import randint

def error_catching(func):
    @wraps(func) #wraps allows pickling of decorators
    def my_func(*args, **kwargs):
        process_number = randint(1,99999)
        while True:
            try:
                return func(process_number, *args, **kwargs)
            except KeyboardInterrupt:
                print("Keyboard interrupt in worker", process_number)
                return
            except Exception as e:
                print("Error in worker {}:\n\t{}\n\tRestarting in 3 seconds...".format(process_number, repr(e)))
                sleep(3)
    return my_func


@error_catching
def f(process_number):
    print("starting worker:", process_number)
    while True:
        # The process defined by this function will repeat these operations indefinitely
        sleep(2)
        print("Worker {} checks in.".format(process_number))


if __name__ == '__main__':
    processes = []

    for i in range(3):
        p = Process(target=f)
        p.daemon = True
        p.start()
        processes.append(p)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt in main")
        sys.exit()
```
Some take-aways that I should remember whilst I designed these scripts are:
- One can not simply add decorator functions to functions that are spawned as a process as this results in a function that cannot be pickled. The solution is to include an additional `wraps` decorator from the `functools` package.
- One should assign daemon flags to daemon processes. Otherwise the processes do not shut down when the main process tries to terminate.
