import { rmSync } from "fs";
import { join } from "path";

import { glob } from "glob";

function removeFilesCallback(err: Error | null, paths: string[]): void {
  paths.forEach((path: string): void => {
    rmSync(path, { force: true, recursive: true });
  });
}

function ignoreFiles(path: string, patterns: string[]): void {
  patterns.forEach((pattern: string): void => {
    glob(join(path, pattern), removeFilesCallback);
  });
}

export { ignoreFiles };
