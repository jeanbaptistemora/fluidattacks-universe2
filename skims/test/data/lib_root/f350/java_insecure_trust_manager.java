import javax.net.ssl.TrustManagerFactory;

public class Test {

	public WebClient insecureClient() {
		try{

			TrustManager my_manager = InsecureTrustManagerFactory.INSTANCE;
			SslContext insecure_context = SslContextBuilder.forClient().trustManager(my_manager).build();
			return insecure_context;

		} catch (Exception e){

			throw new RuntimeException(":: An error ocurred in ssl", e);

		}
	}

	public WebClient secureClient() {
		try{
			TrustManager my_sec_manager = trustManagerFactory.getTrustManagers();
			SslContext secure_context = SslContextBuilder.forClient().trustManager(my_sec_manager).build();
			return secure_context;

		} catch (Exception e){

			throw new RuntimeException(":: An error ocurred in ssl", e);

		}
	}
}
