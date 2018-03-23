/*
Script that gives responsive capabilities to every table of the site,
as long as its class is one of the three predefined (tb-row, tb-col, tb-alt).
It is used to offer a general solution to responsive tables that does not
hurt design, like making it scrollable.
It covers the main types of tables, horizontally and vertically distributed
and a particular one, a table with two columns where the content is alternated
*/

(function($) {
  $.fn.transpose = function() {
    var diff = $(this)[0].rows[0].cells.length - $(this)[0].rows.length;
    if (diff > 0) {
      for (i = 0; i < diff; i++) {
        this[0].insertRow(-1);
      }
    }
    var newrows = [];
    for (j = 0; j < $(this)[0].rows[0].cells.length; j++) {
      newrows[j] = "";
      for (z = 0 ; z < $(this)[0].rows.length; z++) {
        newrows[j] += $(this)[0].rows[z].innerHTML.split("\n")[j + 1] + "\n";
      }
    }
    for (i = 0; i < $(this)[0].rows.length; i++) {
      $(this)[0].rows[i].innerHTML = "\n" + newrows[i] + "\n";
    }
    if (diff < 0) {
      for (i = 0; i < Math.abs(diff); i++) {
        this[0].deleteRow(-1);
      }
    }
    else if (diff > 0) {
      for (i = 0; i < $(this)[0].rows.length; i++) {
        this[0].rows[i].innerHTML = this[0].rows[i].innerHTML.replace(/undefined\n/g, '');
      }
    }
  };
})(jQuery);

(function($) {
  $.fn.swap = function() {
    var temp;
    for (i = 1; i < $(this)[0].rows.length; i+=2) {
      temp = $(this)[0].rows[i].cells[0].innerHTML;
      $(this)[0].rows[i].cells[0].innerHTML = $(this)[0].rows[i].cells[1].innerHTML;
      $(this)[0].rows[i].cells[1].innerHTML = temp;
    }
  };
})(jQuery);

function responsive(tableclass, minsize, maxsize){
  table = $(document).find(tableclass);
  $(table).each(function () {
    if ($(this)[0].rows[0].cells[$(this)[0].rows[0].cells.length - 1].offsetWidth < minsize && !$(this).hasClass("tb-responsive")) {
      if (tableclass == ".tb-col") {
        $(this).transpose();
      }
      if (tableclass == ".tb-alt") {
        $(this).swap();
      }
      $(this).toggleClass("tb-responsive");
    }
    else {
      if (tableclass == ".tb-col") {
        if ($(this)[0].rows[0].cells[0].offsetWidth > maxsize * $(this)[0].rows.length && $(this).hasClass("tb-responsive")) {
          $(this).transpose();
          $(this).toggleClass("tb-responsive");
        }
      }
      else if ($(this)[0].rows[0].cells[0].offsetWidth > maxsize * $(this)[0].rows[0].cells.length && $(this).hasClass("tb-responsive")) {
        if (tableclass == ".tb-alt") {
          $(this).swap();
        }
        $(this).toggleClass("tb-responsive");
      }
    }
  });
}

(function($) {
  $(window).on('resize', function(){
    responsive(".tb-row", 180, 200);
    responsive(".tb-col", 180, 200);
    responsive(".tb-alt", 260, 280);
  });
})(jQuery);

$(document).ready(function() {
  responsive(".tb-row", 180, 200);
  responsive(".tb-col", 180, 200);
  responsive(".tb-alt", 260, 280);
});
