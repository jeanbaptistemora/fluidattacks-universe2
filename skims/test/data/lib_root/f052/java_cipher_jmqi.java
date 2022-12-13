import com.ibm.mq.*;
import com.ibm.mq.jmqi.JmqiUtils;
import org.apache.log4j.Logger;

class Test {

	private final String cipherSuite = "TLS_RSA_WITH_AES_128_CBC_SHA256";

	public void insecure() {
		JmqiUtils.toCipherSuite(cipherSuite);
	}

	public void secure() {
		String safeSuite = "TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256";
		JmqiUtils.toCipherSuite(safeSuite);
	}

}
