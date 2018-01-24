$(document).ready(function(){

	/* Add Hexagon Effect */

	var hexagon 	= 	$(".hexagon-white").html();
						$("#reasons-carousel .item").prepend("<div class='svg'>"+hexagon+"</div>");
						$(".xp-icon figure").prepend($(".hexagon-white, .hexagon-gradient"));

	/* Carousels */

	$('#brands-carousel').owlCarousel({
		
		loop: true,
		margin: 10,
		nav: false,
		responsive:{
			0:{ items:1 },
			600:{ items:3 },
			1000:{ items:4 }
		}

	});

	$('#reasons-carousel').owlCarousel({

		nav: false,
		dots: false,
		loop: true,
		center: true,
		touchDrag: false,
		mouseDrag: false,
		pullDrag: false,
		autoWidth: false,
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