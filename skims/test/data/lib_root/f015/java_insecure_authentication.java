import AnyOtherClass;

public class MustFail {
  public void objectCreation() {
    HttpHeaders instantiatedHeaders = new HttpHeaders();
    instantiatedHeaders.setBasicAuth();
  }
  public void parameter(HttpHeaders parameterHeaders) {
    parameterHeaders.setBasicAuth();
  }
  public void fromGetHeaders(){
    AnyClass anyObject;

    anyObject = request.getHeaders();
    anyObject.setBasicAuth();
  }
}

public class MustNotFail {
  public void objectCreation() {
    AnyOtherClass instantiatedHeaders = new AnyOtherClass();
    instantiatedHeaders.setBasicAuth();
  }
  public void parameter(AnyOtherClass parameterHeaders) {
    parameterHeaders.setBasicAuth();
  }
  public void fromGetHeaders(){
    AnyClass anyObject;

    anyObject = request.getNoHeaders();
    anyObject.setBasicAuth();
  }
}
