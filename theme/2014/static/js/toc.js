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

function sideClass() {
  $(".toc").toggleClass("sidetable");
  $(".intro-header").toggleClass("side");
  $(".contbody").toggleClass("side");
  $(".footer").toggleClass("side");
}

function insert(ToC) {
  var toc = $(".toc");
  if ($(window).width() < 945) {
    if ($(toc).length) {
      if ($(toc).hasClass("sidetable")) {
        $(toc).insertAfter("h1");
        sideClass();
      }
    }
    else {
      $(ToC).insertAfter("h1");
    }
  }
  else {
    if ($(toc).length) {
      if (!$(toc).hasClass("sidetable")) {
        $(toc).appendTo(".row");
        sideClass();
      }
    }
    else {
      $(ToC).appendTo(".row");
      sideClass();
    }
  }
}

var newitem = ""
$(document).ready(function () {

  // Set title depending of page language
  if ($(".language")[0].innerHTML == "en ") {
    var ToC = "<div class=\"toc\"><nav class=\"table-of-contents\">" + "<h2>Content</h2>" + "<ol class=\"arabic\">";
  }
  else {
    var ToC = "<div class=\"toc\"><nav class=\"table-of-contents\">" + "<h2>Contenido</h2>" + "<ol class=\"arabic\">";
  }

  // Build the Table of Content
  getinfo(".sect1", "h2", ".sect2", "loweralpha");

  // Insert Table of Content after main header
  ToC += newitem + "</nav></div>";
  insert(ToC);
});

$(document).scroll(function () {
  var ScrollTop = $(document).scrollTop();
  if (ScrollTop == 0 && $(".side-scrolled").length) {
    $(".sidetable").toggleClass("side-scrolled");
  }
  else if (ScrollTop > 0 && !$(".side-scrolled").length) {
    $(".sidetable").toggleClass("side-scrolled");
  }

  $(".anchor").each(function(){
    var Top = $(this).offset().top;
    var diff = ScrollTop - Top;
    var TocLink = $("li > a[href*='#"+ this.id +"']:not(.anchor-sign)");
    if ((diff > -50) && (diff < 0)) {
      if ($("li > a[class*='active-block']").length) {
        $("li > a[class*='active-block']").toggleClass("active-block");
      }
      $(TocLink).toggleClass("active-block");
    }
    if ($(TocLink).hasClass("active-block") && diff < -60) {
      $(TocLink).toggleClass("active-block");
      $($(TocLink).parent()[0].previousSibling).children("a").toggleClass("active-block");
    }
  });
});

(function($) {
  $(window).on('resize', function() {
    insert(0);
  });
})(jQuery);
