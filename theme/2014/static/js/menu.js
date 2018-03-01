/*
Script that makes the navigationbar responsive in small screens,
organizing the content in a dropdown menu.
*/

(function($) {

  $.fn.menumaker = function(options) {
      
      var cssmenu = $(this), settings = $.extend({
        title: "Menu",
        format: "dropdown",
        sticky: false
      }, options);

      return this.each(function() {
        cssmenu.prepend('<div class="menu-button">' + settings.title + '</div>');
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

        resizeFix = function() {
          var mainmenu = cssmenu.find('.menu-button');
          var submenu = cssmenu.find('.submenu-button');
          if ($( window ).width() >= 955) {
            if (!cssmenu.children('ul').hasClass('m-opened')) {
              cssmenu.children('ul').toggleClass('m-opened')
            }
            if (!cssmenu.find('ul li ul').hasClass('sm-opened')) {
              cssmenu.find('ul li ul').toggleClass('sm-opened')
            }
          }

          if ($(window).width() < 955) {
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
       title: "Menu",
       format: "multitoggle"
    });
  });
})(jQuery);

$(document).scroll(function () {
  var ScrollTop = $(document).scrollTop();
  if (ScrollTop == 0 && $(".css-scrolled").length) {
    $(".css-scrolled").toggleClass("css-scrolled");
    $(".m-scrolled").toggleClass("m-scrolled");
    $(".has-sub-scrolled").toggleClass("has-sub-scrolled");    
  }
  else if (ScrollTop > 0 && !$(".css-scrolled").length) {
    $(".cssmenu").toggleClass("css-scrolled");
    $(".m-opened").toggleClass("m-scrolled");
    $(".has-sub").toggleClass("has-sub-scrolled");
  }
});