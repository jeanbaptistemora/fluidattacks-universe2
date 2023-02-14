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
