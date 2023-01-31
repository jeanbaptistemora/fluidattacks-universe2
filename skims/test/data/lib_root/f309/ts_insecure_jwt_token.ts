
import jwt from 'jsonwebtoken';

export function unsafeJwt<T extends Object> (payload: T): string {
    const privateKey: string = "mykey";
    let allowed_algos: Array<string> = ['none', 'hs256'];
    const options: jwt.SignOptions = { expiresIn: 10000, algorithms:  allowed_algos};
    try {
      return jwt.sign(payload, privateKey, options);
    } catch (e) {
      throw new Error(e.message);
    }
}

export function safeJwt<T extends Object> (payload: T): string {
    const privateKey: string = "mykey";
    let allowed_algos: Array<string> = ['hs256'];
    const options: jwt.SignOptions = { expiresIn: 10000, issuer: "None", algorithms:  allowed_algos};
    try {
      return jwt.sign(payload, privateKey, options)
    } catch (e) {
      throw new Error(e.message)
    }
}
