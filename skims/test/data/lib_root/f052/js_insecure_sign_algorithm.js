var jwt = require('jsonwebtoken');

// Case 0: Plain implementation. Must mark line 14.

const payload = {
  sub: "1234567890",
  name: "John Doe",
  manager: true
};

const secretKey = 'secret';

let token = jwt.sign(payload, secretKey, {
    algorithm: 'HS256',
    expiresIn: '10m'
});

// Case 1: Options as external object. Must mark line 22.

let optObj = {
  expiresIn: '5s',
  algorithm: 'HS256',
  otherOption: 7,
}

token = jwt.sign(payload, secretKey, optObj);


// Case 2: Options as external object. Must mark line 22.

var someAlgorithm = 'HS256';

let optObj2 ={
  expiresIn: '5s',
  algorithm: someAlgorithm,
  otherOption: 7,
}

token = jwt.sign(payload, secretKey, optObj2);

// Case 3: Default algorithm. If no Algorithm especified HS256 is used
// So, it should be marked, here, line 44 must be marked:

token = jwt.sign(payload, secretKey, {
  expiresIn: '10m'
});
