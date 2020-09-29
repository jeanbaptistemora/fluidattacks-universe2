const babelParser = require("@babel/parser");
const fs = require("fs");

function parse(target) {
  const content = fs.readFileSync(target, "utf8");
  // https://babeljs.io/docs/en/babel-parser
  const parseTree = babelParser.parse(content, {
    allowAwaitOutsideFunction: true,
    allowImportExportEverywhere: true,
    allowReturnOutsideFunction: true,
    allowSuperOutsideMethod: true,
    allowUndeclaredExports: true,
    errorRecovery: true,
    plugins: [
      "asyncGenerators",
      "bigInt",
      "classPrivateMethods",
      "classPrivateProperties",
      "classProperties",
      "doExpressions",
      "dynamicImport",
      "estree",
      "exportDefaultFrom",
      "exportNamespaceFrom",
      "functionBind",
      "functionSent",
      "importMeta",
      "jsx",
      "logicalAssignment",
      "nullishCoalescingOperator",
      "numericSeparator",
      "objectRestSpread",
      "optionalCatchBinding",
      "optionalChaining",
      "partialApplication",
      "throwExpressions",
      "topLevelAwait",
      "typescript",
      "v8intrinsic",
      {
        decorators: {
          decoratorsBeforeExport: true,
        },
      },
      {
        pipelineOperator: {
          proposal: "smart",
        },
      },
    ],
    sourceType: "module",
    startLine: 1,
  });
  const parseTreeJson = JSON.stringify(parseTree, null, 2);

  process.stdout.write(parseTreeJson);
}

function cli() {
  const path = require('yargs').demandCommand(1).argv._[0];
  parse(path);
}

cli()
