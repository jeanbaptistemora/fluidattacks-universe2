var jwt = require("jsonwebtoken");

// Case 0: Plain implementation. Must mark line 14.

const payload = {
  sub: "1234567890",
  name: "John Doe",
  manager: true,
};

const secretKey = "secret";

let token = jwt.sign(payload, secretKey, {
  algorithm: "HS256",
  expiresIn: "10m",
});

// Case 1: Options as external object. Must mark line 22.

let optObj = {
  expiresIn: "5s",
  algorithm: "HS256",
  otherOption: 7,
};

token = jwt.sign(payload, secretKey, optObj);

// Case 2: Async implementation with no options.
// Line 31 must be marked.

token = jwt.sign({ foo: "bar" }, privateKey, function (err, token) {
  console.log(token);
});

// Case 3: Default algorithm. If no Algorithm especified HS256 is used
// So, it should be marked, here, line 44 must be marked:

token = jwt.sign(payload, secretKey, {
  expiresIn: "10m",
});

// Control cases (No line should be marked:

// SafeCase 0: Plain implementation with safe alg.

token = jwt.sign(payload, secretKey, {
  algorithm: "HS512",
  expiresIn: "10m",
});

// SafeCase 1: Other instances with .sign method

token = someLibrary.sign(payload, secretKey, {
  algorithm: "HS256",
  expiresIn: "10m",
});

// SafeCase 2: Other method:

token = jwt.signa(payload, secretKey, {
  algorithm: "HS256",
  expiresIn: "10m",
});
