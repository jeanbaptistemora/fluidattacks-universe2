const jwt = require('jsonwebtoken');

function unsafeVerifyJwt() {
    // The signature is not verified before decoding
    let allowed_algos = ['PS384'];
    jwt.decode(token, key, allowed_algos);
}

function safeVerifyJwt() {
    // The jwt is verified before being decoded
    let allowed_algos = ['PS384'];
    const verify_config = { expiresIn: 10000, algorithms:  allowed_algos};
    jwt.verify(token_secure, key, verify_config);
    jwt.decode(token_secure, key, allowed_algos);
}
