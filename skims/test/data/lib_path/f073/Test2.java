public class Test2 implements Pipe<Xxx> {

  @Override
  public Xxx process(Xxx message) {
    switch (inputCore.ghi()) {
      case AB:
        abc.def(locationInfo.getEmail());
        abc.def(locationInfo.getEmail());
        break;
      case CD:
      case EF:
      default:
        abc.def(address.getMainDescription());
        break;
    }
    switch (inputCore.ghi()) {
      case CD:
      case EF:
      default:
        abc.def(address.getMainDescription());
        break;
    }
    switch (inputCore.ghi()) {
      case AB:
        abc.def(locationInfo.getEmail());
        abc.def(locationInfo.getEmail());
        break;
      case CD:
      case "default":
    }
    switch (inputCore.ghi()) {}
    return message;
  }
}
