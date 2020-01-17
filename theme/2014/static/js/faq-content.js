//Add basic styles for active tabs
$('.accordion-item-title').on('click', function() {
    $(this).addClass('red');
    $(this).parent('.accordion-item').siblings().find('.accordion-item-title').removeClass('red');
  });

(function($){
    $(document).ready(function(){
        // Add acordion item class
        $( ".sect3" ).addClass("accordion-item")

        // Accordion section
        $( "h4" ).addClass("accordion-item-title db pv3 link black hover-red pointer black");

        // Section content
        $( ".sect3 > div" ).addClass("accordion-content bb b--black-20 pl3-l");

        $( ".accordion-item-title").click(function() {
            $(this).nextAll( ".accordion-content" ).toggle( "active" );
          });
    });
})(jQuery);
