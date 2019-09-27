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

    //quoteblocks
    $( ".quoteblock" ).addClass("overflow-auto bl b--dark-blue bw2 i tc pv4 ph2 bg-fluid-lightgray");

    //pre-formatted text
    $( "pre" ).addClass("overflow-auto bl b--dark-blue bw2 tl f5 pa3 bg-fluid-lightgray ma0");

    //tooltips
    $ ( ".tooltip-text" ).addClass("bg-tooltip shadow-4 white absolute z-3 f6 w-maxcontent ph2 tc hideme mt4");

    $( ".tooltip" ).addClass("bb black relative");

    //tag cloud tags
    $( ".tag-1" ).addClass("f1");
    $( ".tag-2" ).addClass("f2");
    $( ".tag-3" ).addClass("f3");
    $( ".tag-4" ).addClass("f4");

    //international tel input
    $( ".intl-tel-input" ).addClass("db");

    //fluid-buttons
    $( ".button" ).addClass("bg-fluid-red br3 white montsy f4 b pa2 hv-fluid-dkred");
    $( "span.button  > a" ).addClass("white");

  });
})(jQuery);
