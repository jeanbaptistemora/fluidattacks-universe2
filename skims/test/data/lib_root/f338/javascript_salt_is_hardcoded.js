import { createHash } from "crypto";

function hashPasswordSecure(password) {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto.createHash("sha256");
  hash.update(password + salt);
  return salt + hash.digest("hex");
}

function hashPassword(password) {
  const salt = "HARDCODED_SALT";
  const hash = createHash("sha256");
  hash.update(password + salt);
  return hash.digest("hex");
}
