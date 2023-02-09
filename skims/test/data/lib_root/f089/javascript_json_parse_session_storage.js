// These lines should be marked due direct usage without validation
const anyString = "key";
const myVar = JSON.parse(sessionStorage.getItem("anyVal"));
const myVar2 = JSON.parse(sessionStorage.getItem(anyString));

// These lines should not be marked, indirect usage is not possible to check whether
// there was a validation
//Applying SymbolicEval to bypass this intended limitation could lead to FPs
const value = sessionStorage.getItem("example");
const result = JSON.parse(value);

const value2 = sessionStorage.getItem("example2");
value3 = anyValidation(value2);
const result2 = JSON.parse(value3);
