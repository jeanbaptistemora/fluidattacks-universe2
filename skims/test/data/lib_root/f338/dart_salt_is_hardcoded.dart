import 'dart:convert';

const String salt = 'HARDCODED_SALT';

String hashPassword(String password) {
  final hash = sha256.convert(utf8.encode(password) + utf8.encode(salt));
  return salt + hash.toString();
}
