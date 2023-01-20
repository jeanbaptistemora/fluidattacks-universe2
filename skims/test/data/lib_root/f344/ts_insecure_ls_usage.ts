// unsafe object
const res = new XMLHttpRequest();
res.open("GET", "http://example.com/test", true);
res.send(null);

// strings storage is allowed (Safe line)
localStorage.setItem("anyKey", "anyStringValue");

// Direct storage with http obj MUST FAIL
localStorage.setItem("unsafe", res.response);
localStorage.setItem("anyKey", res.responseText);

// JSON.parse usage with http obj MUST FAIL
localStorage.setItem("unsafe", JSON.stringify(res.response));
