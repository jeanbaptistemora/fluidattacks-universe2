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
          if (mainmenu.hasClass('m-open')) { 
            mainmenu.hide().removeClass('m-open');
          }
          else {
            mainmenu.show().addClass('m-open');
            if (settings.format === "dropdown") {
              mainmenu.find('ul').show();
            }
          }
        });

        cssmenu.find('li ul').parent().addClass('has-sub');

        multiTg = function() {
          cssmenu.find(".has-sub").prepend('<span class="submenu-button"></span>');
          cssmenu.find('.submenu-button').on('click', function() {
            $(this).toggleClass('submenu-opened');
            if ($(this).siblings('ul').hasClass('sm-open')) {
              $(this).siblings('ul').removeClass('sm-open').hide();
            }
            else {
              $(this).siblings('ul').addClass('sm-open').show();
            }
          });
        };

        if (settings.format === 'multitoggle') multiTg();
        else cssmenu.addClass('dropdown');

        if (settings.sticky === true) cssmenu.css('position', 'fixed');

        resizeFix = function() {
          var mainmenu = cssmenu.find('.menu-button');
          var submenu = cssmenu.find('.submenu-button');
          if ($( window ).width() > 1100) {       
            cssmenu.children('ul').addClass('m-open').show();
            cssmenu.find('ul li ul').addClass('sm-open').show();
          }

          if ($(window).width() < 1100) {
            cssmenu.children('ul').removeClass('m-open').hide();
            cssmenu.find('ul li ul').removeClass('sm-open').hide();
            if (mainmenu.hasClass('menu-opened')) {
              mainmenu.removeClass('menu-opened');
            }
            if (submenu.hasClass('submenu-opened')) {
              submenu.removeClass('submenu-opened');
            }
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

$(document).ready(function() {	
	$( ".widget h2" ).click(
		function() {
			$(this).parent().toggleClass('active');
		}
	);	  	
});
