const jwt = require('jsonwebtoken');

function unsafeVerifyJwt() {
    // The signature is not verify before decoding
    const sign_config = { algorithm: 'RS256'};
    let token = jwt.sign(payload, key, sign_config);

    let allowed_algos = ['RS256'];
    jwt.decode(token, key, allowed_algos);
}

function safeVerifyJwt() {
    let safe_algo = "PS384";
    let token_secure = jwt.sign(payload, key, {algorithm: safe_algo});

    let allowed_algos = ['PS384'];
    const verify_config = { expiresIn: 10000, algorithms:  allowed_algos};
    jwt.verify(token_secure, key, verify_config);

    jwt.decode(token_secure, key, allowed_algos);
}
