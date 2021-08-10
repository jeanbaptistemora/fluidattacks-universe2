package f073

fun main() {
    val x = 1
    when (x) {
        1 -> print("Case 1")
        2 -> print("Case 2")
    }

    when (x) {
        3 -> print("Case 3")
        else -> print("Default case 1")
    }

    when (x) {
        4 -> print("Empty else block")
        else -> {}
    }

    when (x) {
        4 -> print("Empty else block with comments")
        else -> {
            // Comment
        }
    }

    when (x) {
        5 -> print("Case 5")
        else -> {
            print("Default case 2")
        }
    }
}
