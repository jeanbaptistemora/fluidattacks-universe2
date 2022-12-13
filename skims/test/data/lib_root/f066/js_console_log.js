
try {
    var a = 1 / 0;
}
catch (err) {
    console.log(`${err}`);
}

try {
    var a = 1 / 0;
}
catch {
    console.log("error");
}

try {
    var a = 1 / 0;
}
catch (err) {
    console.log(err);
}

try {
    var a = 1 / 0;
}
catch (err) {
    console.log("error");
    console.warn(err);
    throw err;
}

try {
    var a = 1 / 0;
}
catch (err) {
    console.log("error" + err);
}

try {
    var a = 1 / 0;
}
catch (err) {
    var b = "error"
    console.log(b);
    console.error(err);
}

