do {}
catch Machine.insufficientFunds(let coinsNeeded) {}
catch Machine.insufficientFunds {}
catch is Machine.insufficientFunds, Machine.insufficientFunds {}
catch let error as NSError { }
catch let error { }
catch { }
