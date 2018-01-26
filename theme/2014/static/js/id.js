(function($) {
  $.fn.idtag = function() {
    for (i = 1; i < 5; i++) {
      var titles = $(document).find("h"+ i +":visible");
      for (j = 0; j < titles.length; j++) {
        var str = titles[j].innerText;
        if (titles[j].id == "" || titles[j].id.indexOf("_") >= 0) {
          str = str.replace(/^[0-9].*\.\s+/, '');
          str = str.replace(/[¡!¿?,':\.]/g, '');
          str = str.replace(/\s+/g, '-').toLowerCase();
          var replaceChars={ "á":"a" ,"é":"e", "í":"i", "ó":"o", "ú":"u", "ñ":"n" };
          str = str.replace(/[áéíóúñ]/g, function(match) {return replaceChars[match];});
          titles[j].id = str;
          $(titles[j]).prepend('<a href="#'+ str +'" class="anchor"></a>');
        }
      }
    }
  };
})(jQuery);

(function($) {
  $(document).ready(function() {
    $(this).idtag();
  });
})(jQuery);

(function($) {
  $(window).on('resize', $(document).idtag);
})(jQuery);

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
