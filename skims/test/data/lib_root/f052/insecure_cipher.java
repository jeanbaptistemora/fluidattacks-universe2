import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;

@Component
public class SslInsecure {
	private static final String SSL="SSL";
	public void SslVerification(boolean disable) {
		try {
			SSLContext unsafecontext = SSLContext.getInstance(SSL);
		} catch (NoSuchAlgorithmException | KeyManagementException e) {
      //Do something
		}
	}
}

@Component
public class SslSecure {
	private static final String SSL="TLSv1.2";
	public void SslVerification(boolean disable) {
		try {
			SSLContext safecontext = SSLContext.getInstance(SSL);
		} catch (NoSuchAlgorithmException | KeyManagementException e) {
      //Do something
		}
	}
}
