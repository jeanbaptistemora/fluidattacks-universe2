// Carousel component options
$(".owl-carousel")
  .owlCarousel({
    autoHeight: false,
    autoWidth: false,
    autoplay: true,
    autoplayTimeout: 2000,
    center: true,
    loop: true,
    responsive: {
      0: { items: 2 },
      600: { items: 3 },
      1000: { items: 5 },
      1600: { items: 8 },
    },
    smartSpeed: 1000,
  });
