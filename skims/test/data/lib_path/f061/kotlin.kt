package f061

fun main() {
    val a = 6
    val b = 0
    var c: Int

    try {
        c = a / b
    } catch (e: ArithmeticException) {
        println(e.message)
    } catch (e: IOException) {
        // Comment
    } catch (e: Exception) {}
}
