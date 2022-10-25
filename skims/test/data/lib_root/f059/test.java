public class Test{
    public void insecure(){
		log.info("Dangerous" + System.getenv()); // Insecure
	}

    public void secure(){
		log.info("Hello world"); // secure
	}
}
