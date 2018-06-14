/*
Script that manages the navigation bar, making it responsive in small screens
by turning it into a drop-down menu.
It also controls the color change in the bar when it is located at the top
of the screen
*/

(function($) {

  $.fn.menumaker = function(options) {

      var cssmenu = $(this), settings = $.extend({
        format: "dropdown",
        sticky: false
      }, options);

      return this.each(function() {
        cssmenu.prepend('<div class="menu-button"></div>');
        $(this).find(".menu-button").on('click', function(){
          $(this).toggleClass('menu-opened');
          var mainmenu = $(this).next('ul');
          mainmenu.toggleClass('m-opened');
        });

        cssmenu.find('li ul').parent().addClass('has-sub');

        multiTg = function() {
          cssmenu.find(".has-sub").prepend('<span class="submenu-button"></span>');
          cssmenu.find('.submenu-button').on('click', function() {
            if ($(window).width() < 865) {
              $(this).toggleClass('submenu-opened');
              $(this).siblings('ul').toggleClass('sm-opened');
            }
          });
        };

        if (settings.format === 'multitoggle') multiTg();
        else cssmenu.addClass('dropdown');

        if (settings.sticky === true) cssmenu.css('position', 'fixed');

        // Change layout depending of window width
        resizeFix = function() {
          var mainmenu = cssmenu.find('.menu-button');
          var submenu = cssmenu.find('.submenu-button');
          if ($( window ).width() >= 825) {
            if (!cssmenu.children('ul').hasClass('m-opened')) {
              cssmenu.children('ul').toggleClass('m-opened')
            }
            if (!cssmenu.find('ul li ul').hasClass('sm-opened')) {
              cssmenu.find('ul li ul').toggleClass('sm-opened')
            }
          }

          if ($(window).width() < 825) {
            cssmenu.children('ul').removeClass('m-opened');
            cssmenu.find('ul li ul').removeClass('sm-opened');
            mainmenu.removeClass('menu-opened');
            submenu.removeClass('submenu-opened');
          }
        };
        resizeFix();
        return $(window).on('resize', resizeFix);

      });
  };
})(jQuery);

(function($){
  $(document).ready(function(){
    $(".cssmenu").menumaker({
       format: "multitoggle"
    });
  });
})(jQuery);
