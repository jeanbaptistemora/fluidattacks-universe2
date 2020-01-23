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
    $( ".button" ).addClass("bg-fluid-red br3 white montsy f4 b pa1 hv-fluid-dkred");
    $( "span.button  > a" ).addClass("white");

    //Add whitespace after a paragraph
    $( ".paragraph" ).addClass("pb3");

    //qanda
    $( ".qlist > ol > li" ).addClass("mb0 pb3");

    //red inner links
    $( "span.inner > a" ).addClass("c-fluid-dkred b hover-bg-light-gray");

    //monokai theme
    $( ".highlight > pre" ).addClass("bg-code-bk ma0 br0 bn tl c-codegray");
    $( ".highlight > pre > span.c, span.cm, span.cp, span.c1, span.cs, span.gu" ).addClass("c-codebrown");
    $( ".highlight > pre > span.err" ).addClass("bg-code-dkred c-codepink");
    $( ".highlight > pre > span.k, span.kc, span.kd, span.kp, span.kr, span.kt, span.no" ).addClass("c-codelightblue");
    $( ".highlight > pre > span.l, span.m, span.mh, span.mf, span.mi, span.mo ,span.se span.il" ).addClass("c-codepurple");
    $( ".highlight > pre > span.n, span.p, span.nb, span.ni, span.nl, span.py ,span.nv span.w span.bp span.vc span.vg span.vi" ).addClass("c-codegray");
    $( ".highlight > pre > span.o, span.kn, span.nt, span.ow, span.gd" ).addClass("c-codelightred");
    $( ".highlight > pre > span.ge" ).addClass("i");
    $( ".highlight > pre > span.gs" ).addClass("b");
    $( ".highlight > pre > span.ld, span.s, span.sb, span.sc, span.sd, span.s2 ,span.sh span.si span.sx span.sr span.s1 span.ss" ).addClass("c-codeyellow");
    $( ".highlight > pre > span.na, span.nc, span.nd, span.ne, span.nf, span.nx, span.gi" ).addClass("c-codegreen");
    $( ".highlighttable" ).addClass("collapse");
    $( ".highlighttable > pre" ).addClass("fs-normal pl3 tl");
    $( ".linenos" ).addClass("bn pa0 v-top");
    $( ".linenos > .linenodiv > pre" ).addClass("bg-code-bk bn br0 ma0 c-codegray");
    $( ".code" ).addClass("bn pa0 w-100");

    //Definitions:
    $( ".hdlist1" ).addClass("f4 b");

    // ulist elements
    // Add style to ulist
    $( ".ulist" ).addClass("mt3 pl3")

    // Add style to ulist items in ul elements
    $( ".ulist > li > p" ).addClass("mt3")

    // Add style to ulist items in div elements
    $( ".ulist > ul > li > p" ).addClass("mt3")

    // Add style to fluid-qanda
    $( ".fluid-qanda > ol > li" ).addClass("i list")

    // Add style to imageblock and videoblock elements
    $( ".imageblock, .videoblock" ).addClass("ma3 tc")

    // Add style to listingblock and literalblock
    $( ".listingblock, .literalblock" ).addClass("mv3 mh0")

    // Add style for images
    $( "img" ).addClass("mw-100 v-mid")

    // Add style to title classes
    $( ".title" ).addClass("f5-l f6 t-grey")

    // Add style to col-lg-8 and col-md-10 classes
    $( ".col-lg-8, .col-md-10" ).addClass("tc w-100")
  });
})(jQuery);
