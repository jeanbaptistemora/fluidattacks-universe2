$(document).ready(function(){

	var current_map = $(".data-map.active").data("map");
	$(".data-map").not(".data-map:first").hide();

	$(".load-map").click(function(){

		var el = $(this);
		var load_map = el.data("map");
		
		$("body,html").stop().animate({scrollTop: $(".map").position().top - 85}, 500, 'swing', function() { });

		if(current_map != load_map){
			
			$(".load-map").removeClass("active");
			el.addClass("active");

			$(".data-map").slideUp();
			$("."+load_map).slideDown();

			current_map = load_map;

		}
		
	});

});