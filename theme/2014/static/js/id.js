/*
Script that takes every HTML <h> tag from <h1> to <h5> of the current page
and uses its text content to create an ID, free of most types of special
characters, so it can be given to a <span> element prepended to the respective
<h> tag in order to be used as an anchor. The creation of the span element
becomes necessary after the menu was fixed to the top of the page, to solve the
offset problem when jumping to the anchor.
A link is also created next to the titles to improve accesibility
*/

(function($) {
  $.fn.idtag = function() {
    for (i = 1; i < 5; i++) {
      var titles = $(document).find("h"+ i +":visible");
      for (j = 0; j < titles.length; j++) {
        if (!($(titles[j]).children(".anchor").length) && !$(titles[j]).parents(".colfoot").length && !$(titles[j]).parents(".benefit-header").length && !$(titles[j]).parents(".header-title").length) {
          var replaceChars={ "á":"a" ,"é":"e", "í":"i", "ó":"o", "ú":"u", "ñ":"n" };
          var str = titles[j].innerText.toLowerCase();
          str = str.replace(/^[0-9.]*\s/, '');
          str = str.replace(/[¡!¿?,':\.]/g, '');
          str = str.replace(/\s+/g, '-');
          str = str.replace(/[áéíóúñ]/g, function(match) {return replaceChars[match];});
          $(titles[j]).prepend('<a href="#'+ str +'" class="anchor-sign f4 top-0"></a>');
          $(titles[j]).prepend('<span id="'+ str +'" class="anchor"></span>');
          $(titles[j]).removeAttr("id");
          if ( titles.length ) {
            str = titles[j].textContent;
            titles[j].childNodes[2].data = str.slice(0,str.toLowerCase().search(/[a-záéíóú]/)) + str[str.toLowerCase().search(/[a-záéíóú]/)].toUpperCase() + str.slice(str.toLowerCase().search(/[a-záéíóú]/) + 1);
          }
        }
      }
    }
  };
})(jQuery);

// Add anchors to pages containing question blocks
(function($){
  $.fn.qtag = function() {
    if ($(".qlist").length) {
      var question = $(".qlist")[0].children[0].children;
      var i = 1;
      $(question).each(function() {
        $(this).prepend('<span id="q'+ i +'" class="anchor"></span>');
        i++;
      });
    }
  };
})(jQuery);

$(document).ready(function() {
  $(this).idtag();
  $(this).qtag();
});

// Fix issues with anchors in Chrome
$(document).ready(function () {
        var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
        if (window.location.hash && isChrome) {
            setTimeout(function () {
                var hash = window.location.hash;
                window.location.hash = "";
                window.location.hash = hash;
            }, 300);
        }
    });
