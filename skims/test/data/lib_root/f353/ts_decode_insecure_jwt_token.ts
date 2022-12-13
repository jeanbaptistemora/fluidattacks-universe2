
import jwt from 'jsonwebtoken';

export function unsafeJwt<T extends Object> (payload: T, privateKey: string): string {
    const options: jwt.SignOptions = { expiresIn: 10000, algorithms:  ['PS384']};
    return jwt.decode(payload, privateKey, options)
}

export function safeJwt<T extends Object> (payload: T, privateKey: string): string {
  const options: jwt.SignOptions = { expiresIn: 10000, algorithms:  ['PS384']};
  try {
    jwt.verify(payload, privateKey, options);
  } catch (e) {
    throw new Error(e.message);
  }
  return jwt.decode(payload, privateKey, options)
}
