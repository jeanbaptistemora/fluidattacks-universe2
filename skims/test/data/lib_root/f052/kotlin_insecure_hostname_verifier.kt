import javax.net.ssl.HostnameVerifier
import javax.net.ssl.SSLSession
import okhttp3.OkHttpClient


val builderNotSafe = OkHttpClient.Builder()
builderNotSafe.hostnameVerifier(object : HostnameVerifier {
  override fun verify(hostname: String?, session: SSLSession?): Boolean {
    return true // Noncompliant (s5527)
  }
})


val builderSafe = okhttp3.OkHttpClient.Builder()
