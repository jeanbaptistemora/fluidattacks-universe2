import fs from "fs";
import { JSDOM } from "jsdom";
import * as yargs from "yargs";
import { exampleGenerator } from "./generators/example";
import { hexbinMapGenerator } from "./generators/hexbinMap";
import { DataType, NodeType } from "./types";

// Required because node.js do not have a DOM yet D3 need it
global.document = new JSDOM("<!DOCTYPE html>").window.document;

interface ICliArguments {
  generator: string;
  height: number;
  sources: string[];
  target: string;
  width: number;
}

const cliArgs: ICliArguments = yargs
  .option("generator", {
    choices: [
      "example",
      "hexbin-map",
    ],
    demandOption: true,
  })
  .option("height", { type: "number", demandOption: true })
  .option("sources", { type: "array", demandOption: true })
  .option("target", { type: "string", demandOption: true })
  .option("width", { type: "number", demandOption: true })
  .coerce("sources", (arg: Array<string | number>)  => (
    arg.map((source: string | number) => fs.readFileSync(source.toString(), "utf-8"))
  ))
  .argv as ICliArguments;

// Compute the required data with the provided generator
let node: NodeType;
let data: DataType;

switch (cliArgs.generator) {
  case "example":
    data = JSON.parse(cliArgs.sources[0]);
    node = exampleGenerator(data, cliArgs.width, cliArgs.height);
    break;
  case "hexbin-map":
    data = {
      points: cliArgs.sources[0],
      topography: cliArgs.sources[1],
    };
    node = hexbinMapGenerator(data, cliArgs.width, cliArgs.height);
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
