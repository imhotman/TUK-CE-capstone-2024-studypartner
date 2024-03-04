// eco_forecast-N3 [hylTa4BFAR]
(function() {
  $(function() {
    $(".eco_forecast-N3").each(function() {
      const $block = $(this);
      // Swiper
      const swiper = new Swiper(".eco_forecast-N3 .contents-swiper", {
        slidesPerView: 1,
        spaceBetween: 0,
        allowTouchMove: false,
        loop: true,
        autoplay: {
          delay: 5000,
        },
        pagination: {
          el: ".eco_forecast-N3 .swiper-pagination",
          clickable: true,
        },
        navigation: {
          nextEl: ".eco_forecast-N3 .swiper-button-next",
          prevEl: ".eco_forecast-N3 .swiper-button-prev",
        },
      });
      // Swiper Play, Pause Button
      const pauseButton = $block.find('.swiper-button-pause');
      const playButton = $block.find('.swiper-button-play');
      playButton.hide();
      pauseButton.show();
      pauseButton.on('click', function() {
        swiper.autoplay.stop();
        playButton.show();
        pauseButton.hide();
      });
      playButton.on('click', function() {
        swiper.autoplay.start();
        playButton.hide();
        pauseButton.show();
      });
    });
  });
})();
// eco_forecast-N6 [IILtA4bFS3]
(function() {
  $(function() {
    $(".eco_forecast-N6").each(function() {
      const $block = $(this);
      // Swiper
      const swiper = new Swiper(".eco_forecast-N6 .contents-swiper", {
        slidesPerView: 1,
        spaceBetween: 0,
        allowTouchMove: false,
        loop: true,
        autoplay: {
          delay: 5000,
        },
        navigation: {
          nextEl: ".eco_forecast-N6 .swiper-button-next",
          prevEl: ".eco_forecast-N6 .swiper-button-prev",
        },
      });
    });
  });
})();