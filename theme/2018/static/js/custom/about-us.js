$(document).ready(function(){
	
	/* Add Hexagon Effect */

	var hexagon 	= 	$(".hexagon-white").html();
						$("#reasons-carousel .item").prepend("<div class='svg'>"+hexagon+"</div>");
						$(".xp-icon figure").prepend($(".hexagon-white, .hexagon-gradient"));

	/* Carousels */

	$('#us-carousel').owlCarousel({
		
		nav:false,
		dots:false,
		loop: false,
		margin:10,
		responsiveClass:true,
		responsive:{
            0:{ items:1 },
            600:{ items:2 },
            1000:{ items:3 }
        }

	});

	$('#reasons-carousel').owlCarousel({

		nav: false,
		dots: false,
		margin: 100,
		loop: true,
		touchDrag: false,
		mouseDrag: false,
		pullDrag: false,
		autoWidth: true,
		items: 1

	});

	$('#reasons-text-carousel').owlCarousel({

		nav:false,
		dots:false,
		margin: 100,
		loop: true,
		touchDrag: false,
		mouseDrag: false,
		pullDrag: false,
		autoWidth: false,
		items: 1

	});

	$('.reasons-carousel-controls .back').click(function() {
		$('#reasons-carousel, #reasons-text-carousel').trigger('prev.owl.carousel');
	});

	$('.reasons-carousel-controls .next').click(function() {
		$('#reasons-carousel, #reasons-text-carousel').trigger('next.owl.carousel');
	});
	
});