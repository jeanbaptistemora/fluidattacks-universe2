// These lines should be marked due direct usage without validation
const anyString = "key";
const myVar = JSON.parse(localStorage.getItem("anyVal"));
const myVar2 = JSON.parse(localStorage.getItem(anyString));

// These lines should not be marked, indirect usage is not possible to check whether
// there was a validation
const value = localStorage.getItem("example");
const result = JSON.parse(value);

const value2 = localStorage.getItem("example2");
value3 = anyValidation(value2);
const result2 = JSON.parse(value3);
