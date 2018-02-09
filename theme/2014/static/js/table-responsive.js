(function ($) {
  $.fn.responsive = function () {
    table = $(document).find(".tb-row");
    $(table).each(function () {
      if ($(this)[0].rows[0].cells[0].offsetWidth < 100) {
        if (!$(this).hasClass("tb-row-responsive")) {
          $(this).toggleClass("tb-row-responsive");         
        }
      }
      else if ($(this)[0].rows[0].cells[0].offsetWidth > 100 * $(this)[0].rows[0].cells.length) {
        if ($(this).hasClass("tb-row-responsive")) {
          $(this).toggleClass("tb-row-responsive");          
        }
      }
    });
  };
})(jQuery);

(function ($) {
  $(window).on('resize', $(document).responsive);
})(jQuery);

$(document).ready(function (){
  $(this).responsive();
});
