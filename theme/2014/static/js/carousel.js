$('.owl-carousel').owlCarousel({
loop:true,
margin:10,
nav:false,
autoWidth:true,
autoplay: true,
smartSpeed: 1000,
autoplayTimeout:2000,
responsive:{
  0:{
      items:1
  },
  600:{
      items:3
  },
  1000:{
      items:5
  }
}
})
