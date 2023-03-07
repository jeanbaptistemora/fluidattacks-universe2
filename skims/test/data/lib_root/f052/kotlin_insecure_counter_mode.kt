import java.security.SecureRandom
import javax.crypto.Cipher
import javax.crypto.spec.GCMParameterSpec
import javax.crypto.spec.SecretKeySpec


fun encrypt(key: ByteArray, ptxt: ByteArray) {
    val nonce: ByteArray = "7cVgr5cbdCZV".toByteArray() // The initialization vector is a static value

    val gcmSpec  = GCMParameterSpec(128, nonce) // The initialization vector is configured here
    val skeySpec = SecretKeySpec(key, "AES")

    val cipher: Cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.ENCRYPT_MODE, skeySpec, gcmSpec) // Noncompliant
}


fun encrypt(key: ByteArray, ptxt: ByteArray) {
        val random: SecureRandom = SecureRandom()
        val nonce: ByteArray     = ByteArray(12)
        random.nextBytes(nonce) // Random 96 bit IV

    val gcmSpec = javax.crypto.spec.GCMParameterSpec(128, nonce, 0, 12)
    val skeySpec = SecretKeySpec(key, "AES")

    val cipher: Cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.ENCRYPT_MODE, skeySpec, gcmSpec)
}
