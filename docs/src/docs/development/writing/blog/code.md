---
id: code
title: Code
sidebar_label: Code
slug: /development/writing/blog/code
---

* **BC01:** We *must* write source code in English,
  including comments.

* **BC02:** We *must* indent with **two spaces** instead of one tab,
  except when the language used requires otherwise.

* **BC03:** We *must* use braces
  following the [Stroustrup style](https://en.wikipedia.org/wiki/Indentation_style#Variant:_Stroustrup)
  (no one-liners; see [an example](https://eslint.org/docs/rules/brace-style#stroustrup)).

* **BC04:** We *must not* write source code lines
  longer than **80 characters**.

* **BC05:** We *must not* leave lines of code
  with [debug comments](https://en.wikipedia.org/wiki/Comment_(computer_programming)#Debugging).

* **BC06:** We *must* separate each function definition with an empty line
  unless the linter or language requires otherwise.

* **BC07:** We *must* enumerate the embedded code snippets.
  (To do so, we add the linenums parameter to the source block.)

* **BC08:** We *must not* have embedded code snippets
  with more than **eight lines**.

* **BC09:** We *must* not repeat a snippet already used in the guide.

* **BC10:** The code snippets *must* be ours.

* **BC11:** We *must* add the lines of code to the blog post
  using a code block, not images.
  Example:

  ```c
  function cool(x) {
    /*Use brief comments in English only when necessary.
    We must explain our code in the document.*/
    int y;
    y = x + 1;
    return y;
    //And don't forget this: no more than eight lines.
  }
  ```

## Explanations

* **BE01:** We *should* include short gifs showing results
  to support the explanations of the procedures (e.g., exploitations)
  under consideration.

* **BE02:** We *must* add a description
  that is less than **80 characters** in length
  for each gif.
  Example:

  ![BE02](https://res.cloudinary.com/fluid-attacks/image/upload/v1624053143/docs/development/writing/bea_pavipm.gif)
  <p align="center">
  Figure x. Example of a description of a gif with exploitation results.
  </p>

* **BE03:** We *must not* give technical explanations
  that are irrelevant to cybersecurity
  (e.g., introducing a programming language
  without mentioning how to use it securely).

> **NOTE:**
> This section of our documentation is under construction.
