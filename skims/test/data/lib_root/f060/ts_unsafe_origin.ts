var iframe = document.getElementById("testiframe");
iframe.contentWindow.postMessage("secret", "*"); // Noncompliant: * is used

var secframe = document.getElementById("testsecureiframe");
secframe.contentWindow.postMessage("hello", "https://secure.example.com"); // Compliant
