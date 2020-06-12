import fs from "fs";
import { JSDOM } from "jsdom";
import * as yargs from "yargs";
import { exampleGenerator } from "./generators/example";
import { DataType, NodeType } from "./types";

// Required because node.js do not have a DOM yet D3 need it
global.document = new JSDOM("<!DOCTYPE html>").window.document;

interface ICliArguments {
  generator: string;
  height: number;
  source: string;
  target: string;
  width: number;
}

const cliArgs: ICliArguments = yargs
  .option("generator", {
    choices: [
      "example",
    ],
    demandOption: true,
  })
  .option("height", { type: "number", demandOption: true })
  .option("source", { type: "string", demandOption: true })
  .option("target", { type: "string", demandOption: true })
  .option("width", { type: "number", demandOption: true })
  .argv;

// Read data from the source file
const data: DataType = JSON.parse(fs.readFileSync(cliArgs.source, "utf-8"));

// Compute the required data with the provided generator
let node: NodeType;
switch (cliArgs.generator) {
  case "example":
    node = exampleGenerator(data, cliArgs.width, cliArgs.height);
    break;
  default:
    node = document.createElement("div");
}

// Write data to the target file
fs.writeFileSync(cliArgs.target, `
  <!DOCTYPE html>
  <body>
    ${node.innerHTML}
  </body>
`);
