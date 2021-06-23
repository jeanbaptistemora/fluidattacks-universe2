class Test{
    public static void main(String[] args) {
        try {
            int a = 30 / 0;
        }
        catch (NullPointerException|Exception e) { log(); }
        catch (java.io.IOException|Exception|ArithmeticException e) { log(); }
        catch (Exception e) { log(); }
    }
}
