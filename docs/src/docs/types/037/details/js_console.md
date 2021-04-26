---
id: js_console
title: JavaScript Console
sidebar_label: JavaScript Console
slug: /types/037/details/js_console
---

In front-end programming,
JavaScript's Console object provides access to the browser's debugging console[^1].
Arguments passed to `log`, `warn` and `error` methods are visible to the user
that is using the website, it's also visible to attackers.

As per Fluid Attacks' criteria[^2] the application must not disclose internal
system information such as stack traces because this information can be
leveraged by to further exploit other vulnerabilities.

Developers tend to do debugging the following way:

```js {3}
try { /* Business logic code goes here ... */ }
catch (err) {
  console.error(err);
}
```

But this ends in lots of information that attackers use to better understand
the inner workings on the system,
aiding them in creating and improving attack vectors.

```log
Error: <rect> attribute x: Expected length, "NaN".
(anonymous) @ cdnjs.cloudflare.com/ajax/libs/d3/5.16.0/d3.min.js:2
Error: <rect> attribute y: Expected length, "NaN".
(anonymous) @ cdnjs.cloudflare.com/ajax/libs/d3/5.16.0/d3.min.js:2
Error: <rect> attribute transform: Expected number, "rotate(NaN, NaN, NaN)".
...
```

[^1]: https://www.w3schools.com/jsref/obj_console.asp
[^2]: https://fluidattacks.com/products/rules/list/077/
