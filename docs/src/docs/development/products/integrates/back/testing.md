---
id: testing
title: Testing
sidebar_label: Testing
slug: /development/products/integrates/backend/testing
---

For the backend, we use the following tests:

- **Unit tests**: Individually test functions or methods and classes.
  Unit tests in Fluid Attacks must be:

  - **Repeatable**:
    Regardless of where they are executed,
    the result must be the same.
  - **Fast**:
    Unit tests should take little time to execute because,
    being the first level of testing,
    where you have isolated functions/methods and classes,
    the answers should be immediate.
    A unit test should take at most two (2) seconds.
  - **Independent**:
    The functions or classes to be tested should be isolated,
    no secondary effect behaviors should be validated,
    and,
    if possible,
    we should avoid calls to external resources such as databases;
    for this, we use mocks.
  - **Descriptive:** For any developer,
    it should be evident what is being tested in the unit test,
    what the result should be,
    and in case of an error,
    what is the source of the error.

- **Functional tests:**
  These tests are focused on the application's business requirements,
  where the result of an action is verified,
  aiming to validate that many integrated functionalities work
  as a whole and perform the execution.
