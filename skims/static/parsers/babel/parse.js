const babelParser = require("@babel/parser");
const fs = require("fs");

function parse(content) {
  // https://babeljs.io/docs/en/babel-parser
  // https://github.com/babel/babel/blob/master/packages/babel-parser/ast/spec.md
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
      ["decorators", {"decoratorsBeforeExport": true}],
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
      ["pipelineOperator", {"proposal": "smart"}],
      "throwExpressions",
      "topLevelAwait",
      "typescript",
      "v8intrinsic",
    ],
    sourceType: "module",
    startLine: 1,
  });
  const parseTreeJson = JSON.stringify(parseTree);

  process.stdout.write(parseTreeJson);
}

// Read from stdin and process it
parse(fs.readFileSync(0).toString())
