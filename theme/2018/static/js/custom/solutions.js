var hexagon = $(".hexagon-white").html();
$(".xp-icon figure").prepend($(".hexagon-white, .hexagon-gradient"));

$('#product-carousel').owlCarousel({
	autoWidth: true,
	margin: 0,
	nav:false,
	dots:false,
	loop: true,
	items: 1
});



$("#btn-fluidasserts").click(function(){
	$('#product-carousel').trigger('to.owl.carousel', 1);
	$("#product-carousel .owl-item p").removeClass("reading");
	$("#product-carousel .owl-item:nth-child(even) p").addClass("reading");
});

$("#btn-fluidintegrates").click(function(){
	$('#product-carousel').trigger('to.owl.carousel', 2);
	$("#product-carousel .owl-item p").removeClass("reading");
	$("#product-carousel .owl-item:nth-child(odd) p").addClass("reading");
});


$('#testimonial-carousel').owlCarousel({
	nav:false,
	dots:false,
	loop: false,
	margin:10,
	responsiveClass:true,
	items: 1
});

$('.testimonial-carousel-back').click(function() {
	$('#testimonial-carousel').trigger('prev.owl.carousel');
});

$('.testimonial-carousel-next').click(function() {
	$('#testimonial-carousel').trigger('next.owl.carousel');
});

/* HOW WE DO IT */

$(document).ready(function(){

	$(".how-we-do-it-content").not(".how-we-do-it-content:first").hide();

	var current_icons = $(".display-hwdi-content.active").data("display");


	$(".display-hwdi-content").click(function(){

		var el = $(this);
		var display = el.data("display");

		$("body,html").stop().animate({scrollTop: $(".how-we-do-it-parent").position().top - 85}, 500, 'swing', function() { });

		if(current_icons != display){

			$(".display-hwdi-content").removeClass("active");
			el.addClass("active");

			$(".how-we-do-it-content").slideUp();
			$(display).slideDown();

			current_icons = display;
		}

	});

});