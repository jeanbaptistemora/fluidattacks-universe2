async function test() {
  (() => {
    switch (new Date().getDay()) {
      case 0:
      case 1:
        day = "Monday";
        break;
    }
    switch (new Date().getDay()) {
      case 0:
      case 1:
        day = "Monday";
        break;
      default:
        day = "Test";
    }
  })()
}
test()
