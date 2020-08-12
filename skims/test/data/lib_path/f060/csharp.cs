try {}
catch (NullReferenceException e) when (e.ParamName == "…") { log() }
catch (NullReferenceException) when (e.ParamName == "…") { log() }
catch (System.ApplicationException) { log() }
catch (System.Exception e) { log() }
catch (SafeException e) { log() }
