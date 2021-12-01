---
slug: road-to-functional-python/
title: Road to Functional Python
date: 2018-07-27
category: programming
subtitle: Functional coding in Python
tags: application, functional, python, multiparadigm
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331067/blog/road-to-functional-python/cover_amvdni.webp
alt: Swiss army knive
description: Here is an intro to the essential aspects of functional
  programming in Python, its benefits, how to start the migration,
  the most used libraries, and more.
keywords: Functional Paradigm, Object-oriented, Stateless,
  Multiparadigm Application, Python, Programming Future,
  Ethical Hacking, Pentesting
author: Oswaldo Parada
writer: oparada
name: Oswaldo José Parada Cuadros
about1: Mechanical Engineer
about2: Family, friends and little details. There is the answer.
source: https://unsplash.com/photos/Y23XUEvgVVE
---

Probably there is nothing better for the spirit than having a hobby that
we are passionate about, that makes us feel in love all the time and
makes us want to return to it. Better, the results obtained while
practicing your hobby, without any intention, becomes a global
phenomenon, used by large and small companies becoming in the source of
income for many. This is how Python came about, a project initially as a
hobby, but over the years has earned a place among the most widely used
languages, not only because is easy to use but for its versatility.
Python has been able to adapt to the frenetic changes in technology and
has been a strong contender in many fields. Today it wants to change
again, it wants to evolve before the same evolution arrives. Today it
wants to be functional\!

## Before putting on shoes

Before starting, I must warn you that this trip is not for beginners.
You will not be able to face functional Python and survive if you do not
know the basic Python. If this is your case, do not feel bad, you can’t
walk if you don’t even know how to stand, so go and scrape your knees in
a Python playground. Also, get some context by reading [Why we go
functional?](/blog/why-we-go-functional/), which is the prequel of this
article. When you think you’re ready, come back to the road, always be
waiting for you.

## Prepare your backpack

Of course we need supplies for the road. But surprise\! If you already
have Python then you are ready to start walking. One of the most
important characteristics of Python is the multiparadigm coding, meaning
that it supports several programing paradigms in its code. Paradigms can
be the object-oriented, procedural, functional, among others. There are
also libraries with functional features such as
[`itertools`](https://docs.python.org/2/library/itertools.html) or
[`functools`](https://docs.python.org/2/library/functools.html) that are
included in the basic installation.

## First baby steps

One of the main characteristics of the functional paradigm is the
possibility to have methods that receive or return code. This is
difficult to understand in some languages but in Python things are
easier, for example:

**First approximation for basic operations in functional Python.**

``` python
def calc (f, x, y):
  return f(x, y)

def subtract (x, y):
  return x - y

def mult (x, y):
  return x * y

calc(subtract, 10, 3) # 7
calc(mult, 2, 4) # 8
```

## Walk

Perhaps the hardest thing to understand in the functional paradigm is
that there are no iterative cycles, so if you have ever programmed in
some object-oriented language you maybe think that without iterative
cycles you can’t do much or you can’t generate short and clean code. You
are right, partially. The functional paradigm doesn’t have something
like a `for` or a `while` loop, but it does have functions that can
replace the behavior of the loops.

Below is a classic example of iterative loops in Python:

**Increment in list elements example.**

``` python
integer_list = [7, 8, 9]

def increment (x):
  return x + 1

def increment_in_list (list):
  result = []
  for integer in list:
    result.append(increment(integer))
  return result

increment_in_list(integer_list) # [8, 9, 10]
```

If we want to do that in a functional way then we can use `map`, a
method that applies a custom function to all the elements of a list.

**Increment in list elements with *map*.**

``` python
integer_list = [7, 8, 9]

def increment (x):
  return x + 1

map(increment, integer_list) # [8, 9, 10]
```

Another function that allows iterative operations is `filter`, which
creates a new list with the elements that return true when certain
function is applied to a list, for example:

***Filter* method example.**

``` python
integer_list = [7, 8, 9]

def greater_than (x, y):
  return True if x > y else False

filter(lambda x: greater_than(x, 7), integer_list) # [8, 9]
```

These are really useful and simple functions to start coding but sadly
also have some limitations, for example, functions to apply to the lists
cannot have more than one input argument. This is not a problem. Soon we
will study even more powerful functional methods.

## Take a break

You’ve come a long way, congratulations\! You have almost all the
knowledge to enter the big leagues, you just have to learn something
else: Lambda expressions, described as one line functions (*anonymous
functions* in other languages). Below we rewrite the [increment in list
elements example](#increment-example) using lambda expressions.

**Increment in list elements with lambda expression.**

``` python
integer_list = [7, 8, 9]

map(lambda x: x + 1,integer_list) # [8, 9, 10]
```

## Run Forrest, Run!

We are now next to world-class athletes and we can learn a lot from
them. One of the most prominent is
[`itertools`](https://docs.python.org/2/library/itertools.html), a
module designed to make efficient loops in iterable objects, based on
languages such as `Haskell` and `SML`. In fact, you already know some
functions of this module like `map` and `filter`, but now they come with
the whole family and on steroids.

Some of the representative methods of this library are:

**Example of some itertools methods.**

``` python
import itertools

lowercases = ['a','b','c']
uppercases = ['A','B','C']
number_as_string = '1111222334'

""" Chain, allows you to concatenate iterative structures """
list(itertools.chain(uppercases, lowercases))
# ['A', 'B', 'C', 'a', 'b', 'c']

""" Permutations, returns the permutations of n elements in an iterable structures """
list(itertools.Permutations(uppercases, 2))
# [('A','B'),('A','C'),('B','A'),('B','C'),('C','A'),('C','B')]

""" Groupby, group up elements of a data structure based on a condition or rule """
[list(g) for k, g in itertools.groupby(number_as_string)]
# [['1', '1', '1', '1'], ['2', '2', '2'], ['3', '3'], ['4']]

""" Repeat, returns an element as many times as specified """
list(itertools.repeat('A',6))
# ['A', 'A', 'A', 'A', 'A', 'A']

""" Islice, returns n elements of an iterative structure """
list(itertools.islice(number_as_string,5))
# ['1', '1', '1', '1', '2']
```

Not all functional approaches in Python are manifested as libraries,
there are also functional features that are achieved by just writing our
code in a certain way. One of these ways is `currying`, which is defined
as the transformation of a function that receives several input
parameters to a sequence of functions that receives a single parameter.
Why would we do this? Well, this is linked with `laziness` and functions
that create functions, currying allows a partially execution of a
function, making runtime more efficient by avoiding the calculation of
every operation from the beginning.

**Example of currying in Python.**

``` python
def curried_product (a):
    def product(b):
        return a * b
    return product

curried_product(2) # function...
curried_product(2)(3)
# 6

mult = curried_product(3) # function...
mult(4)
# 12
```

## Learning to fly

Now we’ll learn something more sophisticated and exclusive than all of
the above. I will teach you
[`functools`](https://docs.python.org/2/library/functools.html), a
module with higher-level functions, created with the specific purpose of
making Python more functional. This module, like
[`itertools`](https://docs.python.org/2/library/itertools.html), is in
the core of Python.

**Example of some functools methods.**

``` python
import functools

""" Partial, generates a function by partially executing an input function """
def multiply(a,b):
  return a * b

partial_multiply = partial(multiply,6)
print(partial_multiply(2)) # 12

""" Reduce, applies a function of 2 input arguments to a data structure """
functools.reduce(lambda x, y: x + y, [1, 2, 3, 4, 5]) # 15

""" Update_wrapper, copy attributes from one function to another """
from functools import update_wrapper
def foo():
  """This is a foo attribute"""
 pass

def bar():
 pass

update_wrapper(bar, foo)
bar.__doc__  # 'This is a foo attribute'
```

You can even find fantastic external libraries that will help you to
raise your code to a higher functional level. Some of them are
[`PyMonad`](https://pypi.org/project/PyMonad/) and
[`Pydash`](https://pydash.readthedocs.io/en/latest/).

## Limit is in your mind

Here we are, the end of our trip together. But the road does not end at
all. We have only taught you how to hit the road but you are the one who
decides where to go. Python is a powerful language driven by thousands
of people around the world who use their free time to create and improve
code for all of us to use. That’s why, daily, the limitations of Python
are disappearing, leaving the limits only in our mind.

<div class="imgblock">

!["Meme about functional Python"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331065/blog/road-to-functional-python/python-meme_j7mtdu.webp)

<div class="title">

Figure 1. What some developers think about multiparadigm coding.

</div>

</div>

Functional Python is about doing things in the most optimal way
possible. The first thing we must change is our way of thinking. Humans
are reluctant to change, we are afraid of the new but from time to time
there are some specimens who open their minds and take risks, those are
who drive humanity to a superior level. Why not take the risk using
functional Python then? We actually took the risk with functional Python
and the result was one of our most awesome and acclaimed products:
Asserts (though, we not longer offer this product).

## Conclusions

Python is a very useful language that collects the best of different
worlds. Due to its multiparadigm nature, it’s not a problem if we
experiment with different paradigms in the same code, and for that
reason we should not limit ourselves to just one. Each paradigm has
advantages and disadvantages.

Possibly your code in Python is object oriented and that’s fine, it’s a
great opportunity to analyze your code and see what you can transform or
create with any of the tools that you have seen here or that you can
learn by yourself. I already told you, the limit is in your mind. Start
refactoring small components to be functional, this will give you more
confidence and change a bit the way you see the world and the way you
solve problems. Nothing more grateful than a good code. A code that over
the years continues efficient and useful, that doesn’t lose validity.
Our advice is to take a deep breath and get on the road to functional
Python.
