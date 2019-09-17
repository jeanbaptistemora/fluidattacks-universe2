$('.owl-carousel').owlCarousel({
loop:true,
margin:10,
nav:false,
autoplay: true,
smartSpeed: 1000,
autoplayTimeout:2000,
responsive:{
  0:{
      items:2
  },
  600:{
      items:3
  },
  1000:{
      items:5
  },
  1600:{
      items:8
  }
}
})
