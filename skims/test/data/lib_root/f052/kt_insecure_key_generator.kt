val keyPairGen1 = KeyPairGenerator.getInstance("RSA")
keyPairGen1.initialize(1024) // Noncompliant


val keyGen1 = KeyGenerator.getInstance("AES")
keyGen1.init(64) // Noncompliant




val keyPairGen6 = KeyPairGenerator.getInstance("RSA")
keyPairGen6.initialize(2048) // Compliant


val keyGen2safe = KeyGenerator.getInstance("AES")
keyGen2safe.init(128) // Compliant
