import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

public class Test {
	public static void connectionSFTP(List<String> date){
		JSch ssh = new JSch();
		Session session = ssh.getSession(ManagementProperties.getValues("USER"), ManagementProperties.getValues("SERVERNAME"), 2);
		java.util.Properties config = new java.util.Properties();
		String check = "No";
		config.put("StrictHostKeyChecking", check);
		session.setConfig(config);
	}
}

public class Test2 {
	public static void connectionSFTP(List<String> date){
		JSch ssh = new JSch();
		Session session = ssh.getSession(ManagementProperties.getValues("USER"), ManagementProperties.getValues("SERVERNAME"), 2);
		java.util.Properties config = new java.util.Properties();
		config.put("StrictHostKeyChecking", "Yes");
		config.put("SomethingElse", "No");
		session.setConfig(config);
	}
}
