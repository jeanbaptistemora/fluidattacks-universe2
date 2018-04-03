/*
Script that uses the <h> tags to build a Table of Contents.
It uses the Asciidoc division in sections to group the related
content.
*/

function getinfo(sect, header, nxt_sect, label) {
  $(sect).each(function() {

    // Locate header and get its text and link
    var h = $(this).children(header);
    var text = h[0].innerText.replace(/^[0-9].*\.\s+/, '');;
    var link = $(h).children("span")[0].id;

    // Populate the Table of Content
    newitem += "<li>" + "<a href=#" + link + ">" + text + "</a>";

    // Repeat the process recursively for subtitles
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

  // Set title depending of page language
  if ($(".language")[0].innerHTML == "en ") {
    var ToC = "<nav class=\"table-of-contents\">" + "<h2>Content</h2>" + "<ol class=\"arabic\">";
  }
  else {
    var ToC = "<nav class=\"table-of-contents\">" + "<h2>Contenido</h2>" + "<ol class=\"arabic\">";
  }

  // Build the Table of Content
  getinfo(".sect1", "h2", ".sect2", "loweralpha");

  // Insert Table of Content after main header
  ToC += newitem + "</nav>";
  $(ToC).insertAfter("h1");
});
