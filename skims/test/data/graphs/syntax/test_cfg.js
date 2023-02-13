import defaultExport from "module-name";
import * as name from "module-name";
import { export1 } from "module-name";
import { export1 as alias1 } from "module-name";
import { export1 , export2 } from "module-name";
import { export1 , export2 as alias2 , alias3 } from "module-name";
import defaultExport, { export1, export2 } from "module-name";
import defaultExport, * as name from "module-name";
import "module-name";
var promise = import("module-name");

// async function
function resolveAfter2Seconds() {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve('resolved');
        }, 2000);
    });
}

async function asyncCall() {
    console.log('calling');
    const result = await resolveAfter2Seconds();
    console.log(result);
    // expected output: "resolved"
}

asyncCall();


// block
var x = 1;
let y = 1;

if (true) {
    var x = 2;
    let y = 2;
}

console.log(x);
// expected output: 2

console.log(y);
// expected output: 1


// break
let i = 0;

while (i < 6) {
    if (i === 3) {
        break;
    }
    i = i + 1;
}

console.log(i);
// expected output: 3


// class
class Polygon {
    constructor(height, width) {
        this.area = height * width;
    }
}

console.log(new Polygon(4, 3).area);
// expected output: 12


// const
const number = 42;

try {
    number = 99;
} catch (err) {
    console.log(err);
    // expected output: TypeError: invalid assignment to const `number'
    // Note - error messages will vary depending on browser
}

console.log(number);
// expected output: 42



// do-while
var result = '';
var k = 0;
do {
    k += 1;
    result += k + ' ';
}
while (k > 0 && k < 5);
// Despite k == 0 this will still loop as it starts off without the test

console.log(result);


// async for
async function* streamAsyncIterable(stream) {
    const reader = stream.getReader();
    try {
        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                return;
            }
            yield value;
        }
    } finally {
        reader.releaseLock();
    }
}
// Fetches data from url and calculates response size using the async generator.
async function getResponseSize(url) {
    const response = await fetch(url);
    // Will hold the size of the response, in bytes.
    let responseSize = 0;
    // The for-await-of loop. Async iterates over each portion of the response.
    for await (const chunk of streamAsyncIterable(response.body)) {
        // Incrementing the total response length.
        responseSize += chunk.length;
    }

    console.log(`Response Size: ${responseSize} bytes`);
    // expected output: "Response Size: 1071472"
    return responseSize;
}
getResponseSize('https://jsonplaceholder.typicode.com/photos');


// for in
var triangle = { a: 1, b: 2, c: 3 };

function ColoredTriangle() {
    this.color = 'red';
}

ColoredTriangle.prototype = triangle;

var obj = new ColoredTriangle();

for (const prop in obj) {
    if (obj.hasOwnProperty(prop)) {
        console.log(`obj.${prop} = ${obj[prop]}`);
    }
}

// Output:
// "obj.color = red"


// for of
const iterable = [10, 20, 30];

for (let value of iterable) {
    value += 1;
    console.log(value);
}


// for
for (let i = 0; i < 9; i++) {
    console.log(i);
    // more statements
}


// if
function testNum(a) {
    let result;
    if (a > 0) {
        result = 'positive';
    } else {
        result = 'NOT positive';
    }
    return result;
}

console.log(testNum(-5));
// expected output: "NOT positive"


// switc
let expr = "Bananas";
switch (expr) {
    case 'Oranges':
        console.log('Oranges are $0.59 a pound.');
        break;
    case 'Apples':
        console.log('Apples are $0.32 a pound.');
        break;
    case 'Bananas':
        console.log('Bananas are $0.48 a pound.');
        break;
    case 'Cherries':
        console.log('Cherries are $3.00 a pound.');
        break;
    case 'Mangoes':
    case 'Papayas':
        console.log('Mangoes and papayas are $2.79 a pound.');
        break;
    default:
        console.log('Sorry, we are out of ' + expr + '.');
}

console.log("Is there anything else you'd like?");


// while
var n = 0;
var x = 0;

while (n < 3) {
    n++;
    x += n;
}


// try catch
try {
    throw 'myException'; // generates an exception
} catch (e) {
    // statements to handle any exceptions
    logMyErrors(e); // pass exception object to error handler
}

// multiple assignments in the same statement
var x, w, z = 1;
x = y = z = 2;

// arrow functions
function resolveAfter3Seconds() {
    var a = new Promise(resolve => {
        setTimeout(() => {
            resolve('resolved');
        }, 3000);
    });
    return a;
}

(a, b) => {
    let chuck = 42;
    return a + b + chuck;
  }

var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
  var user = req.params['user'];
  res.render('index', { title: 'Express' });
});

express.Router().call('/users')
console.log('hello');

const {
  exec
} = require("child_process");

const collectD = (name, func) => {
    return async (...args) => {
      const end = st.startTimer({ t: name })
      const res = await func(...args)
      end()
      return res
    }
}

app.use(['/safe', '/sec'], securityTxt({
    contact: config.get('sec.contact'),
    languages: [...new Set(locales.map(locale => locale.key.substr(0, 2)))].join(', '),
    expires: security.toUTCString(),
}))

for (const { name, exclude } of autoModels) {
    console.log(name, exclude);
}

arguments[0] = arguments[0].replace(/a href="([^"]+?)"/gi, "hello");

function generateWait() {
    $("#generate-wait").fadeOut(500, () => {});
}

if (!(key in service[ourService])) {
    service[ourService][key] = [];
}

export let name1, name2;
export const name3 = 1, name4 = 2;
export function functionName() { /* … */ }
export class ClassName { /* … */ }
export function* generatorFunctionName() { /* … */ }
export const { name5, name2: bar } = o;
export const [ name6, name7 ] = array;

// Export list
export { variable1 as name9, variable2 as name10, nameN };
export { variable1 as named };
export { name1 as default};

// Default exports
export default function functionName() { /* … */ }

// Aggregating modules
export { import1 as name1, import2 as name2, /* …, */ nameN } from "module-name";

//JSX element
const App = () => {
    const createMarkup = () => {
      return {
        __html: "<img onerror='alert();' src='invalid-image' />",
      };
    };
    return (
      <div>
        <div data={createMarkup()}/>
      </div>
    );
  };
