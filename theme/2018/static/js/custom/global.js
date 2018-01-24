function navbarSolid(){
	var scrollPosition = $(this).scrollTop();
	if(scrollPosition > 85){
		$(".main-navbar").addClass("scrolled");
	}else{
		$(".main-navbar").removeClass("scrolled");
	};
}

/* Scroll events */
$(window).scroll(function(){
	/* Add class to navbar menu when it's scrolled */
	navbarSolid();
});

/* Search for carousel contronls */
$(document).ready(function(){

	$(".carousel-control").click(function(){

		var carousel 	= $(this).data("carousel");
		var direction 	= $(this).data("direction");

		$(carousel).trigger(direction + '.owl.carousel');

	});

});