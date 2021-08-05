package f052

import java.security.NoSuchAlgorithmException
import java.security.spec.ECGenParameterSpec
import java.security.spec.RSAKeyGenParameterSpec
import javax.crypto.Cipher
import javax.crypto.NoSuchPaddingException

class test {
    fun main(args: Array<String>) {
        try {
            val c1 = Cipher.getInstance("AES")
            val c2 = Cipher.getInstance("DES")
            val c3 = Cipher.getInstance("DESede")
            val c4 = Cipher.getInstance("RSA")
            val c5 = Cipher.getInstance("AES/CBC/PKCS5Padding")
            val c6 = Cipher.getInstance("AES/CBC/NoPadding")
            val c7 = Cipher.getInstance("AES/ECB/NoPadding")
            val c8 = Cipher.getInstance("AES/ECB/PKCS5Padding")
            val c9 = Cipher.getInstance("DES/CBC/NoPadding")
            val c10 = Cipher.getInstance("DES/CBC/PKCS5Padding")
            val c11 = Cipher.getInstance("DES/ECB/NoPadding")
            val c12 = Cipher.getInstance("DES/ECB/PKCS5Padding")
            val c13 = Cipher.getInstance("DESede/CBC/NoPadding")
            val c14 = Cipher.getInstance("DESede/CBC/PKCS5Padding")
            val c15 = Cipher.getInstance("DESede/ECB/NoPadding")
            val c16 = Cipher.getInstance("DESede/ECB/PKCS5Padding")
            val c17 = Cipher.getInstance("RSA/ECB/PKCS1Padding")
            val c18 = Cipher.getInstance("RSA/ECB/OAEPWithSHA-1AndMGF1Padding")
            val c19 = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding")

            val k1 = RSAKeyGenParameterSpec(2048, RSAKeyGenParameterSpec.F4)
            val k2 = RSAKeyGenParameterSpec(2047, RSAKeyGenParameterSpec.F4)
            val k3 = ECGenParameterSpec("secp521r1")
            val k4 = ECGenParameterSpec("c2pnb208w1")
        } catch (e: NoSuchAlgorithmException) {
        } catch (e: NoSuchPaddingException) {
        }
    }
}
