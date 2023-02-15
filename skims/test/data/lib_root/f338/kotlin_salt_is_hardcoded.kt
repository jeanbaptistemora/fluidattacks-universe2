import java.security.MessageDigest
import java.util.*

fun main() {
    val password = "myPassword"
    val salt = generateSalt()
    val saltedHash = hashPassword(password, salt)
    println("Salted Hash: $saltedHash")
}

fun generateSalt(): String {
    val sr = SecureRandom.getInstanceStrong()
    val salt = ByteArray(16)
    sr.nextBytes(salt)
    return Base64.getEncoder().encodeToString(salt)
}

fun hashPassword(password: String, salt: String): String {
    val md = MessageDigest.getInstance("SHA-256")
    md.update(salt.toByteArray())
    val hashedPassword = md.digest(password.toByteArray())
    return Base64.getEncoder().encodeToString(hashedPassword)
}




private val SALT = "HARDCODED_SALT"

fun hashPasswordInsecure(password: String): String {
    val md = MessageDigest.getInstance("SHA-256")
    md.update(SALT.toByteArray())
    val hashedPassword = md.digest(password.toByteArray())
    return Base64.getEncoder().encodeToString(hashedPassword)
}
