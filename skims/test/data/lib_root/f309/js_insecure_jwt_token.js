const jwt = require('jsonwebtoken');

function unsafejwt() {
    // Default value of algorithm is vulnerable
    let utoken = jwt.sign(payload, key);

    const sign_config = { algorithm: 'none'};
    let token = jwt.sign(payload, key, sign_config);

    let allowed_algos = ['HS256', 'none'];
    const verify_config = { expiresIn: 10000, algorithms:  allowed_algos};
    jwt.verify(token, key, verify_config);

}

function safejwt() {
    let safe_algo = "PS384";
    let token_secure = jwt.sign(payload, key, {algorithm: safe_algo, issuer: "none"});

    let allowed_algos = ['PS384'];
    const verify_config = { expiresIn: 10000, algorithms:  allowed_algos};
    jwt.verify(token, key, verify_config);

}
