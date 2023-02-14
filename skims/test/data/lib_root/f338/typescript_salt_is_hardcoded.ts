import * as crypto from 'crypto';

function hashPassword(password: string): string {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.createHash('sha256');
  hash.update(password + salt);
  return salt + hash.digest('hex');
}


function hashPasswordHardcoded(password: string): string {
  const salt = "HARDCODED_SALT";
  const hash = crypto.createHash('sha256');
  hash.update(password + salt);
  return hash.digest('hex');
}
