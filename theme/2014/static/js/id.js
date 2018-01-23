(function($) {
  $.fn.idtag = function() {
    for (i = 1; i < 5; i++) {
      var titles = $(document).find("h"+ i +":visible");
      for (j = 0; j < titles.length; j++) {
        var str = titles[j].innerText;
        if (titles[j].id == "" || titles[j].id.indexOf("_") >= 0) {
          str = str.replace(/\s+/g, '-').toLowerCase();
          var replaceChars={ "á":"a" ,"é":"e", "í":"i", "ó":"o", "ú":"u" };
          str = str.replace(/[áéíóú]/g, function(match) {return replaceChars[match];});
          titles[j].id = str;
          $(titles[j]).prepend('<a href="./#'+ str +'" class="anchor"></a>');
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
