val sr_vuln = SecureRandom()
val seed = 123456L
sr_vuln.setSeed(seed) // Noncompliant

val bytearray = "abcdefghijklmnop".toByteArray(charset("us-ascii"))
val sr = SecureRandom(bytearray) // Noncompliant

val sr = SecureRandom() //Compliant

val v = sr.nextInt()
