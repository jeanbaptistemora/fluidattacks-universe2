class OpTransactionRepoAdapter(db: DynamoDbClient)
    extends OpTransactionRepository
    with Logger {

  override def getOpTransaction(
      transactionIdentifier: String
  )(implicit ctx: Context): EitherT[Task, OpError, OpTransaction] = {
    loggerDebug(
      s"getOpTransaction called with transaction identifier: $transactionIdentifier "
    )
    val result: Task[Either[OpError, OpTransaction]] = Task
      .fromTry(
        Try {
          db.query(GenericDynamoDAO.buildQueryRequest())
        }
      )
      .onErrorRecover {
        case e: NullPointerException =>
          loggerError(s"DB error response: NullPointerException")
          Left(OpResourceNotFoundError("Session doesn't exist", None))
        case e: Exception =>
          loggerError(s"DB error response: ${e.getMessage}")
          Left(OpTechnicalError(e.getMessage, None))
      }
    EitherT(result)
  }
}
