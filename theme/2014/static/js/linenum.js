/*
Script used so the line numbers of different code blocks
in an article follow a sequential order instead of
reseting to 1 every time a new code block is declared.
It also resets numbering if the code has a title.
*/

$(document).ready(function () {
  var lines = document.getElementsByClassName("linenodiv");
  if (lines.length) {
    for (i = 1; i < lines.length; i++) {
      // Resets if code block has title
      if ($(lines[i]).parents(".content").prev().length) {}
      // Follows sequential order if not
      else {
        var linenum = lines[i].innerHTML.split('\n').length;
        var newlinenum = "";
        var lastnum = parseInt(lines[i-1].innerHTML.split('\n')[lines[i-1].innerHTML.split('\n').length - 1].replace(/\D/g, ''));
        for (j = 1; j <= linenum; j++) {
          var num = lastnum + j;
          newlinenum += num.toString();
          if (j != linenum) {
            newlinenum += '\n';
          }
        }
        lines[i].innerHTML = "<pre>" + newlinenum + "</pre>";
      }
    }
  }
});
