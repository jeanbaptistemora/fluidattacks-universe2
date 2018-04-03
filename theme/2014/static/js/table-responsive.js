/*
Script that gives responsive capabilities to every table of the site,
as long as its class is one of the three predefined (tb-row, tb-col, tb-alt).
It is used to offer a general solution to responsive tables that does not
hurt design, like making it scrollable.
It covers the main types of tables, horizontally and vertically distributed
and a particular one, a table with two columns where the content is alternated
*/

// Function that transposes a table, incuding cell styles.
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
        newrows[j] += "<t" + $(this)[0].rows[z].innerHTML.split("<t")[j + 1];
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

// Function that alternates the content of the cells in odd rows of a table
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
    if (tableclass == ".tb-alt") {
      // tb-alt enters and leaves responsive mode if the width of its cells is
      // lower or higher than a defined size, respectively
      if ($(this)[0].rows[0].cells[$(this)[0].rows[0].cells.length - 1].offsetWidth < minsize && !$(this).hasClass("tb-responsive")) {
        $(this).swap();
        $(this).toggleClass("tb-responsive");
      }
      if ($(this)[0].rows[0].cells[0].offsetWidth > maxsize * 2 && $(this).hasClass("tb-responsive")) {
        $(this).swap();
        $(this).toggleClass("tb-responsive");
      }
    }
    else {
      // tb-row and tb-col enter responsive mode when their left and right
      // margins differ in more than 5 pixels (since they are centered).
      // It also takes into account the offset if the table is in a list.
      var left = $(this)[0].offsetLeft;
      var right = $(window).width() - $(this)[0].offsetWidth - left + 20 * $(this).parents("li").length;
      if (left - right > 5) {
        if (tableclass == ".tb-col") {
          $(this).transpose();
        }
        $(this).toggleClass("tb-responsive");
      }
      // This tables leave responsive mode if the width of its cells is higher
      // than a defined size or if its higher than 800 pixels (for long tables)
      else if ((($(this)[0].rows[0].cells[0].offsetWidth > maxsize * $(this)[0].rows[0].cells.length) || ($(this)[0].offsetWidth > 800)) && $(this).hasClass("tb-responsive")) {
        if (tableclass == ".tb-col") {
          $(this).transpose();
        }
        $(this).toggleClass("tb-responsive");
      }
    }
  });
}

// Set responsive if the resize requieres it
(function($) {
  $(window).on('resize', function(){
    responsive(".tb-row", 0, 200);
    responsive(".tb-col", 0, 200);
    responsive(".tb-alt", 300, 305);
  });
})(jQuery);

// Set responsive if the width of the device requires it
$(document).ready(function() {
  responsive(".tb-row", 0, 200);
  responsive(".tb-col", 0, 200);
  responsive(".tb-alt", 300, 305);
});
