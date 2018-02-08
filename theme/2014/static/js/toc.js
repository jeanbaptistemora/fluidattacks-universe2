function getinfo(sect, header, nxt_sect, label) {
  $(sect).each(function() {
    var h = $(this).children(header);
    var text = h[0].innerText;
    var link = $(h).children("span")[0].id;
    newitem += "<li>" + "<a href=#" + link + ">" + text + "</a>";
    if ($(this).find(nxt_sect).length) {
      newitem += "<ol class=\""+ label + "\">";
      getinfo($(this).find(nxt_sect), "h" + (parseInt(header[1]) + 1).toString(), ".sect" + (parseInt(nxt_sect[5]) + 1).toString(), "lowerroman");
    }
    newitem += "</li>";
  });
  newitem += "</ol>";
}

var newitem = ""
$(document).ready(function () {
  var ToC = "<nav class=\"table-of-contents\">" + "<h2>Table of Contents</h2>" + "<ol class=\"arabic\">";
  getinfo(".sect1", "h2", ".sect2", "loweralpha");
  ToC += newitem + "</nav>";
  $(ToC).insertAfter("h1");
});
