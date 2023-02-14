---
id: quality
title: Quality
sidebar_label: Quality
slug: /development/values/quality
---

## Testing

As a team and a company,
we are committed to creating quality software,
so every piece of code we create must be tested.
**What do we achieve with this?**

- Identify if the developed functionality behaves correctly.

- Reveal unnecessary complexity in the code,
  such as functions with many lines,
  multiple calls to other functions,
  or a large number of loops.

- Identify security problems.

- Identify scalability issues.

This way,
we develop quality code and detect errors
or bugs before going to production,
reducing reprocesses and affecting
the experience of customers and users.

Within the development process,
our developers must build the corresponding
tests according to the functionality
they are developing;
this guarantees that everything that
is built is tested at different levels.

At `Fluid Attacks'`,
we use **Test-Driven Development**
or **TDD** as our methodology;
with this and our CI/CD practices,
we always make quality part of our development.

## Test-driven development (TDD)

It is a methodology used in software engineering,
which consists of a three-step cycle:

- Write tests to validate what we expect
  from our functionality and have them fail
  (Test First Development).

- Write enough code for these tests to pass.

- Refactoring developing from the needs that
  arise while repeating the cycle.

![TDD steps](https://res.cloudinary.com/fluid-attacks/image/upload/v1676369649/docs/development/values/process_tdd.jpg)

The purpose of TDD is to be able to achieve:

- Clean and working code.

- Avoid unnecessary code.

- Generate more confidence in the written code.

- The Code must comply with the requirements that have been established.

To do TDD we must:

- **Create the test:**
  The developer creates the precise test
  to validate a specific functionality.
  Since they are writing tests based on the
  assumption of how the code will work,
  they are bound to fail at the beginning.

- **Write the implementation:**
  Write the most straightforward code to make the test work.

- **Execute the test:**
  Verify that the test works correctly.

- **Code refactoring:**
  Once the test is successfully executed,
  look for possible code optimizations to
  improve performance.

You should click here to see the different
types of tests that are applied in the Backend
and here to see the ones applied in the Frontend.

## Example of how to implement TDD

We need to design a function that validates
the name of the files that customers upload in
different processes while using our product;
we will use TDD for this:

- We write a test that validates what we require and fails.
  For this example, we create the test in
  `/integrates/back/test/unit/src/new_utils/test_validations.py`

```python
def test_validate_file_name() -> None:
    good_name = "good_name"
    bad_name = "bad_name"
    assert validate_file_name(good_name)
    assert not validate_file_name(bad_name)

```

- To follow the structure of the repository,
  specifying that we will find the function we are going to test
  `/integrates/back/src/new_utils/validations.py`
  The first version of our function is:

```python
def validate_file_name(name: str) -> None:
    pass

```

When we run the test,
it fails as expected:

![Test fail](https://res.cloudinary.com/fluid-attacks/image/upload/v1676375093/docs/development/values/failed.png)

The test fails because our function does not yet
return values that allow us to validate its behavior.

- Now let's write the code necessary for our test to work,
  leave our test the same  and modify our function.

```python
def validate_file_name(name: str) -> bool:
    if name == "good_name":
        return True
    else:
        return False

```

Now our function returns a boolean that,
in the case of receiving as parameter (name) "good_name,"
will be True and otherwise False;
when testing it,
our test is successful.

![Test succesful](https://res.cloudinary.com/fluid-attacks/image/upload/v1676375620/docs/development/values/succesful.png)

- Now it is time to refactor;
  we already have a structure with a known
  parameter (name) that works;
  we need to think about how this parameter
  can change and affect our function.
  Additionally,
  we must ask ourselves:
  what makes a file name invalid or incorrect?
  For this example,
  the definition of a valid name will be that
  it does not contain the following special characters:
  `!, @,#,$,%,^,&,*`
  this will be validated using regular expressions:

```python
import re
def validate_file_name(name: str) -> bool:
    if re.search("[!@#$%^&*]", name):
        return False
    return True

```

If we run our test without changes,
it fails because when we call our
function with the argument **"bad_name,"**
our function returns **True**
since this name does not contain any
of the characters considered invalid.

![second fail](https://res.cloudinary.com/fluid-attacks/image/upload/v1676379764/docs/development/values/secod_filed.png)

- Let's modify our test to validate what happens
  in case the arguments contain them.

```python
def test_validate_file_name() -> None:
    good_name = "good_name"
    bad_name = "bad_name@#"
    assert validate_file_name(good_name)
    assert not validate_file_name(bad_name)

```

![passed](https://res.cloudinary.com/fluid-attacks/image/upload/v1676381578/docs/development/values/passed.png)

- Now we have a function that corresponds to the
  requirements established in the design;
  the cycle can keep repeating,
  as new needs or restrictions are identified,
  for example,
  files have extensions such as .jpg,
  .py.
  yaml,
  how should this be handled?
  Is the length of the file name relevant?
  Should it be considered invalid beyond a certain length?
  Do we prefer our function to return False
  if the file has an invalid name,
  or is it preferable to raise an exception?
  All these questions will lead us to iterate
  on our code to improve and meet the requirements.
