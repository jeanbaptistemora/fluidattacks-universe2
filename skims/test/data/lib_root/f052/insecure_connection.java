@Component
public class InsecureConnection {
	private static final String TLS_1_1=TlsVersion.TLS_1_1;
	public void TlsVerification() {
		try {
			ConnectionSpec spec = new ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
      			.tlsVersions(TlsVersion.TLS_1_1) // Noncompliant
      			.build();
		} catch (NoSuchAlgorithmException | KeyManagementException e) {
      		//Do something
		}
		try {
			ConnectionSpec spec = new ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
      			.tlsVersions(TLS_1_1) // Noncompliant
      			.build();
		} catch (NoSuchAlgorithmException | KeyManagementException e) {
			//Do something
		}
	}
}

@Component
public class SecureConnection {
	private static final String TLS_1_2=TlsVersion.TLS_1_2;
	public void TlsVerification() {
		try {
			ConnectionSpec spec = new ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
      			.tlsVersions(TlsVersion.TLS_1_2) // Compliant
      			.build();
		} catch (NoSuchAlgorithmException | KeyManagementException e) {
      		//Do something
		}
		try {
			ConnectionSpec spec = new ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
      			.tlsVersions(TLS_1_2) // Compliant
      			.build();
		} catch (NoSuchAlgorithmException | KeyManagementException e) {
			//Do something
		}
	}
}
