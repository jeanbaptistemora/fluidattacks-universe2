// unsafe object
const xhr = new XMLHttpRequest();
xhr.open("GET", "http://example.com/test", true);
xhr.send(null);

function handler() {
  if (this.status == 200 && this.responseXML != null) {
    localStorage.setItem("response", this.responseXML);
  }
}

var client = new XMLHttpRequest();

client.onload = handler;

client.onload = () => {
  localStorage.setItem("response", this.responseXML);
};

// safe
client.onload = () => {
  localStorage.setItem("response", this.responseXML);
};
