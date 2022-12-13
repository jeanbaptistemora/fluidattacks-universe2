import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

public class Insecureconfigs {
	public static void connection1(){
		JSch ssh = new JSch();
		Session session = ssh.getSession(ManagementProperties.getValues("USER"), ManagementProperties.getValues("SERVERNAME"), 2);
		java.util.Properties config = new java.util.Properties();
		String check = "No";
		config.put("StrictHostKeyChecking", check);
		session.setConfig(config);
	}

	public static void connection2(){
		JSch ssh = new JSch();
		session = ssh.getSession( Utils.DEFAULT_USER, value.getPublicIpAddress() );
		session.setConfig("StrictHostKeyChecking", "No");
		session.connect();
	}

}

public class Secureconfigs {
	public static void connectionSFTP(){
		JSch ssh = new JSch();
		Session session = ssh.getSession(Utils.DEFAULT_USER, value.getPublicIpAddress());
		java.util.Properties config = new java.util.Properties();
		config.put("StrictHostKeyChecking", "Yes");
		config.put("SomethingElse", "No");
		session.setConfig(config);
	}
}
