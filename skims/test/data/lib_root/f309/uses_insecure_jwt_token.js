const jwt = require('jsonwebtoken');

function unsafejwt() {
    const sign_config = { algorithm: 'none' };
    let token = jwt.sign(payload, key, sign_config);

    let allowed_algos = ['RS256', 'none'];
    const verify_config = { expiresIn: 10000, algorithms:  allowed_algos};
    jwt.verify(token, key, verify_config);

}

function safejwt() {
    let safe_algo = "HS256";
    let token_secure = jwt.sign(payload, key, {algorithm: safe_algo, issuer: "none"});

    let allowed_algos = ['RS256'];
    const verify_config = { expiresIn: 10000, algorithms:  allowed_algos};
    jwt.verify(token, key, verify_config);

}
