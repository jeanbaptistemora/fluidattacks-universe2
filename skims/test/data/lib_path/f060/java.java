try {}
catch (NullPointerException|Exception e) { log() }
catch (java.io.IOException|Exception|ArithmeticException) { log() }
catch (Exception e) { log() }
catch (Exception) { log() }
