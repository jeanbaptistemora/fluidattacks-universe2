// unsafe object
const xhr = new XMLHttpRequest();
xhr.open("GET", "http://example.com/test", true);
xhr.send(null);

// strings storage is allowed (Safe line)
localStorage.setItem("anyKey", "anyStringValue");

// Direct storage with http obj MUST FAIL
localStorage.setItem("unsafe", xhr.response);
localStorage.setItem("anyKey", xhr.responseText);

// JSON.parse usage with http obj MUST FAIL
localStorage.setItem("unsafe", JSON.stringify(xhr.response));
