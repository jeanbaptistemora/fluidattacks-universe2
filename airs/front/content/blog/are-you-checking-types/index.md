---
slug: are-you-checking-types/
title: Are You Checking Types?
date: 2018-08-03
category: programming
subtitle: Static type checking with mypy
tags: application, functional, python, mypy
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330665/blog/are-you-checking-types/cover_wrwgye.webp
alt: Snake checking a code
description: What are the potential problems of untyped objects in Python?
  Here we work on the importance of checking types before running
  the code and how mypy can help.
keywords: Functional Paradigm, Object Oriented, Stateless, Type Checking,
  Python, Duck Typing, Mypy, Ethical Hacking, Pentesting
author: Oswaldo Parada
writer: oparada
name: Oswaldo José Parada Cuadros
about1: Mechanical Engineer
about2: Family, friends and little details. There is the answer.
source: https://unsplash.com/photos/ieic5Tq8YMk
---

The dominoes game is simple, there are 28 tiles (standard version), each
one with a unique combination of two numbers of pips between 0 and 6.
The game’s objective is to be the first player to place all the own
tiles on the table. For this, each player takes turns to place a tile
adjacent to those already on the table as long as the number of pips
matches. Most people believe that dominoes is more a game of luck than
anything else. In fact, it’s a game of strategy. A good player checks
the tiles on the table, counting how many pieces of a certain number of
pips are already placed and which ones the opponents have. By knowing
this, they can choose the best tile to place and force the opponents to
play in a certain way. So, if you always bite the dust in the dominoes,
maybe it’s because you’re not checking enough.

## Ludopathy

We can relate the coding in Python with a game of dominoes. The script
is the tiles on the table, so the players are the developers. The tiles
would be small pieces of code. Again, developers take turns to place
tiles. However, the goal now is that all players win\! So, they can put
in a single script all the code tiles they have. The final result would
be a perfectly coupled script specially assembled to do a certain task.
But if everyone can win, then everyone can lose. And if your developers'
team is already used to constantly losing games, then, just like in
dominoes, you’re not checking enough\!

<div class="imgblock">

![Family playing dominoes](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330662/blog/are-you-checking-types/dominoes_xtbi5m.webp)

<div class="title">

Figure 1. Dominoes can be compared with the development activity.

</div>

</div>

## Bankruptcy

There are many reasons why you can lose in the coding-in-Python game,
but not checking well is one of the most common. Specifically, I’m
talking about checking the type of variables or data structures in your
code.

For example:

**Add integers method in Python..**

``` Python
def add_integers(a, b):
  return a + b

add_integers(2, 3) # 5
```

At first sight, the function seems fine. It works as expected, but it
has a huge problem. In the following example, we’ll use the same
\\add\_integers\\ method, but we’ll make a change.

**Adding strings..**

``` Python
add_integers('2', '3')  #  '23'
```

The code still works as it should be, but it’s not the result we
expected; we managed to "cheat" the function to add strings instead of
integers.

I know this doesn’t say much, but I’ll show you the destructive
potential of this feature with another example using the same
[*add\_integers*](#adding-integers) function:

**A more complex application with no variable typing..**

``` Python
def taxes_calculation(apple_price, taxes_rate):
  return apple_price * taxes_rate

def apples_sale(n_apples, apple_price):
  initial_price = n_apples * apple_price
  taxes = taxes_calculation(initial_price, 0.16)
  result = add_integers(initial_price, taxes)
  return result

apples_sale(3, 20) # 69.6

# Nothing bad until here, but what if we…

apples_sale('3','20') # TypeError: can't multiply
sequence by non-int of type 'str'
```

Now you can cry. Your apple sales business went bankrupt by simply
changing the type of input variables.

## Oh, the irony

Dear reader, if you’re a pythonista who doesn’t allow yourself to be
surprised so easily, you may be saying: *"Wait, what? Python is a
program with dynamic typing; that’s its point, I don’t have to define
the type of variables because the interpreter can understand what the
type is."* Yes, that’s true, but the interpreter is not guilty of having
an entanglement of thousands of methods that depend on each other. The
interpreter is not guilty that any method can modify the state,
including the variable type.

I’ll give you the solution now: Go functional and set the type of your
variables\! If you want to know how to do that, keep reading.

## Canard à l’orange

Many scholars call the typing in Python "duck typing." The name comes
from this premise: "If it goes like a duck and it quacks like a duck,
then it must be a duck." In this way, we understood that Python knows
what the type is by analyzing the behavior and attributes of a variable.
Honestly, in `Fluid Attacks`, we prefer the *Canard à l’orange* ("duck
with orange" in French) instead of living with it in our code.

## How to pluck a duck?

We already know why we shouldn’t let the interpreter choose what type of
variable we’re working with. It may sound a little laborious to have to
type each variable, but this task is easy in Python 3:

**Add integers method with typed variables..**

``` python
def add_integers (a: int , b: int) -> int:
   return a +  b

add_integers(2 , 3) # 5
```

Let’s see if this solves the problem:

**The cruel reality..**

``` python
add_integers('2', '3') # '23'
```

I lied to you again. Typing variables in Python doesn’t do anything to
how the code is executed. Python is like a child who believes everything
you tell him; no matter if you set the type or not, it’ll continue to
obey.  the code and how mypy can help.

## Mypy to the rescue

Setting variable types is useful when we use a tool that has become
popular among the pythonistas: [`mypy`](http://http://mypy-lang.org/).
Mypy is a static type checker. It uses the type hints defined in the
code to validate that these hints are met in the parts of the code where
the variables are used. This tool runs separately from the execution of
the code.

You can use the following command to install mypy in Python 3:

**Mypy installation..**

``` bash
python3 -m pip install mypy
```

Now, we just have to make sure that the code we want to check is saved
in a script and then run the following command:

**Command to use mypy..**

``` bash
python3 -m mypy name_of_my_file.py
```

Let’s go back to the example of \<\<\\adding-integers\\\>\> and save it
in a script called *add\_integer\_method.py*. Now we use mypy:

**Using mypy in a known script..**

``` bash
python3 -m mypy  add_integer_method.py
#... No output
```

If there’s no output when running the command, the code is correct and
can be executed. Now we add the \<\<\\adding-strings, adding strings
example\\\>\> to the file and run mypy again:

**Warnings..**

``` bash
$ python3 -m mypy  add_integer_method.py

# add_integer_method.py:4: error: Argument 1 to "add_integers"
has incompatible type "str"; expected "int"
# add_integer_method.py:4: error: Argument 2 to "add_integers"
has incompatible type "str"; expected "int"
```

Eureka\! Mypy was able to discover that we set a string into a method
that was defined with integer type inputs. Here we use a very small and
maybe obvious example, but imagine applications of thousands of code
lines. Now, with a single command, we can check the variable types.

## Conclusions

We demonstrated the importance of setting the variables' types that
we’ll use and showed how fatal it’s to not check them. Mypy is a
useful tool in any development activity, but it’s especially powerful in
projects where more than one developer contributes. With mypy, we can
debug easier or ensure that code with the wrong types is not deployed to
production. Of course, Mypy is not a straitjacket; this library doesn’t
impose anything on us; we decide to ignore or solve the warnings it
shows us. Finally, we make the recommendation to implement functional
code in your programs; this will make your code more durable, cleaner
and easier to debug. This programming paradigm takes on more versatility
when merged with tools like mypy, which turns very tedious processes
into a matter of seconds. If you still don’t know much about functional
programming in general or functional programming in Python, we invite
you to read the posts ["Why We Go
Functional?"](../why-we-go-functional/)\# and ["Road to Functional
Python"](../road-to-functional-python/)\#. You already have the
knowledge, so will you check types?
