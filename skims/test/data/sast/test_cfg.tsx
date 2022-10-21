//Primitive types and other advanced types

const helloWorld = "Hello World";
var hello: string = "Hello";

const myUser = {
  name: "Sabrina",
};

const passingResponse: [string, number] = ["{}", 200];

const exampleUsers = [{ name: "Brian" }, { name: "Fahrooq" }] as const;


type StringArray = Array<string>;
type NumberArray = Array<number>;
type ObjectWithNameArray = Array<{ name: string }>;

type Ball = {
  diameter: number;
}

interface BirdInterface {
  wings: 2;
}

type Owl = { nocturnal: true } & BirdInterface;

interface Chicken extends BirdInterface {
  colourful: false;
  flies: false;
}

enum StatusCodes {
  OK = 200,
  BadRequest = 400,
  Unauthorized,
  PaymentRequired,
  Forbidden,
  NotFound,
}

const currentStatus = StatusCodes.OK;

interface ArtworkSearchResponse {
  artists: {
    name: string;
    artworks: {
      name: string;
      deathdate: string | null;
      bio: string;
    }[];
  }[];
}

type ErrorWithMessage = {
    error: object
}

function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
  return (
    typeof error === 'object' &&
    error !== null &&
    'message' in error &&
    typeof (error as Record<string, unknown>).message === 'string'
  )
}

const enum MouseAction {
  MouseDown,
  MouseUpOutside,
  MouseUpInside,
}

type PotentialString = string | undefined | null;

type StaffAccount = [number, string, string, string?];

const staff: StaffAccount[] = [
  [0, "Adankwo", "adankwo.e@"],
  [1, "Kanokwan", "kanokwan.s@"],
  [2, "Aneurin", "aneurin.s@", "Supervisor"],
];

type PayStubs = [StaffAccount, ...number[]];

const payStubs: PayStubs[] = [
  [staff[0], 250],
  [staff[1], 250, 260],
  [staff[0], 300, 300, 300],
];

const monthOnePayments = payStubs[0][1] + payStubs[1][1] + payStubs[2][1];

//CONTROL STRUCTURES

let createBall = (diameter: number) => ({ diameter });
let createSphere = (diameter: number, useInches: boolean) => {
  return { diameter: useInches ? diameter * 0.39 : diameter };
};

declare function allowsAnyString(arg: string): PotentialString;
declare function getIDNumber(): string;

const userID = getIDNumber();
console.log("User Logged in: ", userID.toUpperCase());

const handleMouseAction = (action: MouseAction) => {
  switch (action) {
    case MouseAction.MouseDown:
      console.log("Mouse Down");
      break;
  }
};

type MyPartialTypeForEdit<Type> = {
  [Property in keyof Type]?: Type[Property];
} & { id: number };

if (passingResponse[1] === 200) {
  const localInfo = JSON.parse(passingResponse[0]);
  console.log(localInfo);
}

[createBall(1), createBall(2)].forEach((ball, _index, _balls) => {
  console.log(ball);
});

declare function calculatePayForEmployee(id: number, ...args: [...number[]]): number;

calculatePayForEmployee(staff[0][0], payStubs[0][1]);
calculatePayForEmployee(staff[1][0], payStubs[1][1], payStubs[1][2]);

type Cat = { meows: true };
type Dog = { barks: true };
type Cheetah = { meows: true; fast: true };
type Wolf = { barks: true; howls: true };

type ExtractDogish<A> = A extends { barks: true } ? A : never;
declare function getID<T extends boolean>(fancy: T): T extends true ? string : number;

let stringReturnValue = getID(true);
let stringOrNumber = getID(Math.random() < 0.5);

function listenForEvent(eventType: "keyboard" | "mouse", handler: (event: InputEvent) => void) { }

const getPI = () => 3.14;

function runFunction(func: () => void) {
  func();
}

const logMyErrors = (e) => console.log(e);

let i = 10;
while (i < 6) {
    if (i === 3) {
        break;
    }
    i = i + 1;
}

let numb = 10;
try {
    numb = 99;
} catch (err) {
    console.log(err);
}

var result = '';
var k = 0;
do {
    k += 1;
    result += k + ' ';
}
while (k > 0 && k < 5);

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
