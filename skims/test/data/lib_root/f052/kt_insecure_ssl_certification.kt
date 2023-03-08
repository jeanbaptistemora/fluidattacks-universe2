

// Create a trust manager that does not validate certificate chains
val trustAllCerts = (object : X509TrustManager {
  @Throws(CertificateException::class)
  override fun checkClientTrusted(chain: Array<java.security.cert.X509Certificate>, authType: String) {
  } // Noncompliant (s4830)

  @Throws(CertificateException::class)
  override fun checkServerTrusted(chain: Array<java.security.cert.X509Certificate>, authType: String) {
  } // Noncompliant (s4830)

  override fun getAcceptedIssuers(): Array<java.security.cert.X509Certificate> {
   return arrayOf()
  }
 })

// Install the all-trusting trust manager
val sslContext = SSLContext.getInstance("TLSv1.2")
sslContext.init(null, trustAllCerts, java.security.SecureRandom())



val sslContextSafe = SSLContext.getInstance("TLSv1.2")
sslContextSafe.init(null, null, java.security.SecureRandom())
