/*
Script used so the line numbers of differente code blocks
in an article follow a sequential order instead of
reseting to 1 every time a new code block is declared.
*/

$(document).ready(function () {
  var lines = document.getElementsByClassName("linenodiv");
  if (lines.length) {
    for (i = 1; i < lines.length; i++) {
      var linenum = lines[i].innerText.split("\n").length - 1;
      var newlinenum = "";
      for (j = 1; j <= linenum; j++) {
        var num = parseInt(lines[i-1].innerText.split("\n")[lines[i-1].innerText.split("\n").length - 2]) + j;
        newlinenum = newlinenum + num.toString() + "\n";
      }
      lines[i].innerHTML = "<pre>" + newlinenum + "</pre>";
    }
  }
});
