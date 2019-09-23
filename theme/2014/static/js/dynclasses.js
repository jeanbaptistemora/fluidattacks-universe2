/*
This script modifies classes, allowing to include
Tachyons classes on dynamically generated content
*/

(function($){
  $(document).ready(function(){

    //monospace
    $( ".monospaced" ).addClass("bg-fluid-lightgray br2 mono pa1");

    //common links
    $( "a").addClass("no-underline");

  });
})(jQuery);
