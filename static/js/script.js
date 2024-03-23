// study_partner-N3 [hylTa4BFAR]
(function() {
  $(function() {
    $(".study_partner-N3").each(function() {
      const $block = $(this);
      // Swiper
      const swiper = new Swiper(".study_partner-N3 .contents-swiper", {
        slidesPerView: 1,
        spaceBetween: 0,
        allowTouchMove: false,
        loop: true,
        autoplay: {
          delay: 5000,
        },
        pagination: {
          el: ".study_partner-N3 .swiper-pagination",
          clickable: true,
        },
        navigation: {
          nextEl: ".study_partner-N3 .swiper-button-next",
          prevEl: ".study_partner-N3 .swiper-button-prev",
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
// study_partner-N6 [IILtA4bFS3]
(function() {
  $(function() {
    $(".study_partner-N6").each(function() {
      const $block = $(this);
      // Swiper
      const swiper = new Swiper(".study_partner-N6 .contents-swiper", {
        slidesPerView: 1,
        spaceBetween: 0,
        allowTouchMove: false,
        loop: true,
        autoplay: {
          delay: 5000,
        },
        navigation: {
          nextEl: ".study_partner-N6 .swiper-button-next",
          prevEl: ".study_partner-N6 .swiper-button-prev",
        },
      });
    });
  });
})();
