import { default as $ } from "jquery";

/*
Script used so the line numbers of different code blocks
in an article follow a sequential order instead of
reseting to 1 every time a new code block is declared.
It also resets numbering if the code has a title.
*/

export const lineNum: (() => void) = (): void => {
  const lines: HTMLCollection = document.getElementsByClassName("linenodiv");
  // tslint:disable-next-line: strict-boolean-expressions
  if (lines.length) {
    let i: number;
    for (i = 1; i < lines.length; i += 1) {
      // Resets if code block has title
      // tslint:disable-next-line: strict-boolean-expressions
      if ($(lines[i])
          .parents(".content")
          // tslint:disable-next-line: no-empty
          .prev().length) {
      } else {
        let linenum: number; linenum = lines[i].innerHTML.split("\n").length;
        let lastnum: number;
        lastnum = parseInt(lines[i - 1].innerHTML.split("\n")[lines[i - 1].innerHTML.split("\n").length - 1]
        .replace(/\D/g, ""),
                           10);
        let j: number;
        let newlinenum: string; newlinenum = "";
        for (j = 1; j <= linenum; j += 1) {
          let num: number; num = lastnum + j;
          newlinenum += num.toString();
          if (j !== linenum) {
            newlinenum += "\n";
          }
        }
        lines[i].innerHTML = `<pre>${newlinenum}</pre>`;
      }
    }
  }
};
