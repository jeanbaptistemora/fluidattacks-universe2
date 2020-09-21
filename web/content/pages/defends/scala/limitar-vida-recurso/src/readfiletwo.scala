import scala.io.Source

object ReadFileTwo {

  def main(args: Array[String]): Unit = {
        val bufferedSource = Source.fromFile("exampletwo.txt")
        for (line <- bufferedSource.getLines) {
           println(line)
        }
    bufferedSource.close
  }
}
