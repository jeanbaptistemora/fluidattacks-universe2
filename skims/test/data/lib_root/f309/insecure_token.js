const jwt = require('jsonwebtoken');
function nonSecureSign() {
    // Noncompliant
    let none_val = "none"

    let token = jwt.sign({ foo: 'bar' }, key, { algorithm: 'none' });

    jwt.verify(token, key, { expiresIn: 360000 * 5, algorithms: ['RS256', 'none'] });

    let token_insecure = jwt.sign({ foo: 'bar' }, key, { algorithm: none_val });

    jwt.verify(token_insecure, key, { expiresIn: 360000 * 5, algorithms: [none_val] });
}


function secureSign() {
    // Compliant
    let alg = "HS256"

    let token_secure = jwt.sign({ foo: 'bar' }, key, { algorithm: 'HS256' });

    jwt.verify(token_secure, key, { expiresIn: 360000 * 5, algorithms: ['HS256'] });

    let token_secure_2 = jwt.sign({ foo: 'bar' }, key, { algorithm: alg });

    jwt.verify(token_secure_2, key, { expiresIn: 360000 * 5, algorithms: [alg] });
}
