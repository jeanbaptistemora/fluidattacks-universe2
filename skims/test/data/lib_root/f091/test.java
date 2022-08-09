public class Test{
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        // Vulnerable
        String param1 = req.getParameter("param1");
        Logger.info("Param1: " + param1 + " " + Logger.getName()); // Noncompliant

        //Secure
        String param2 = req.getParameter("param2");
        param2 = param2.replaceAll("[\n\r\t]", "_");
        Logger.info("Param1: " + param2 + " " + Logger.getName());
    }
}
