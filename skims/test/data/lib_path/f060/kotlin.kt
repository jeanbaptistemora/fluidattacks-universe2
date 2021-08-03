package f060

fun main() {
    val a = 6
    val b = 0
    var c: Int

    try {
        c = a / b
    } catch (e: ArithmeticException) {
        println(e.message)
    } catch (e: Error) {
        println(e.message)
    } catch (e: Exception) {
        println(e.message)
    } catch (e: Throwable) {
        println(e.message)
    }
}
