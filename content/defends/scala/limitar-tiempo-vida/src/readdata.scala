def readData(): Unit = {
    val bufferSize: Int = 16 * 1024
    val zeroes: Byte = Array.ofDim[Byte](bufferSize)
    val buffer: ByteBuffer = ByteBuffer.allocateDirect(bufferSize)
    try {
      for (rdr <- managed((new FileInputStream("file")).getChannel))
        while (rdr.read(buffer) > 0) {

          // Hacer algo con el búfer

          buffer.clear()           
          buffer.put(zeroes) // sobrescribir el búfer con ceros
          buffer.clear()
        }


    } catch {
      case e: Throwable => {}

    }
}