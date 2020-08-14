do { }
catch Machine.insufficientFunds(let coinsNeeded) { log() }
catch Machine.insufficientFunds { log() }
catch is Machine.insufficientFunds, Machine.insufficientFunds { log() }
catch let error as NSError { log() }
catch let error { log() }
catch { log() }
