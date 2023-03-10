
val bytesIV = "7cVgr5cbdCZVw5WY".toByteArray(charset("UTF-8")) // Predictable / hardcoded IV

val iv = IvParameterSpec(bytesIV)
val skeySpec = SecretKeySpec(secretKey.toByteArray(), "AES")

val cipher: Cipher = Cipher.getInstance("AES/CBC/PKCS5PADDING")
cipher.init(Cipher.ENCRYPT_MODE, skeySpec, iv) // Noncompliant (s3329)

val encryptedBytes: ByteArray = cipher.doFinal("foo".toByteArray())
