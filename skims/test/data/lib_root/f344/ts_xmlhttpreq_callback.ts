// unsafe object
const client = new XMLHttpRequest();
client.open("GET", "http://example.com/test", true);
client.send(null);

const handler = () =>  {
  let value = "SafeValue";
  if (this.status == 200 && this.responseXML != null) {
    // line 10 must be marked
    localStorage.setItem("response", this.responseXML);
    localStorage.setItem("safe", value);
  }
}

client.onload = handler;

client.onload = () => {
  // Line 19 must be marked
  localStorage.setItem("response", this.responseXML);
};

//Safe
localStorage.setItem("safeKey", "safeValue");


