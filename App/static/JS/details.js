document.addEventListener('DOMContentLoaded', function() {
    if ($('.gallery-carousel').length) {
      $('.gallery-carousel').slick({
        dots: true,
        infinite: true,
        speed: 300,
        slidesToShow: 1,
        centerMode: true,
        centerPadding: '60px',
        adaptiveHeight: true,
        arrows: true,
        prevArrow: '<button type="button" class="slick-prev"><i class="fas fa-chevron-left"></i></button>',
        nextArrow: '<button type="button" class="slick-next"><i class="fas fa-chevron-right"></i></button>',
        responsive: [{
          breakpoint: 768,
          settings: {
            centerMode: false,
            centerPadding: '0px'
          }
        }]
      });
    }

    const reviewCount = document.querySelectorAll('.comment').length;
    const rcEl = document.getElementById('reviewCount');
    const ccEl = document.getElementById('commentCount');
    if (rcEl) rcEl.textContent = reviewCount;
    if (ccEl) ccEl.textContent = reviewCount;
  
    //for star rating
    const stars = document.querySelectorAll('.star-rating i');
    function highlightStars(rating) {
      stars.forEach(star => {
        const value = star.getAttribute('data-rating');
        star.classList.toggle('fas', value <= rating);
        star.classList.toggle('far', value >  rating);
      });
    }
    stars.forEach(star => {
        //mouseover to highlight stars
      star.addEventListener('mouseover', () => {
        highlightStars(star.getAttribute('data-rating'));
      });

      star.addEventListener('click', () => {
        document.getElementById('ratingValue').value = star.getAttribute('data-rating');
      });
    });
    //reset stars when mouse leaves stars
    const starContainer = document.querySelector('.star-rating');
    if (starContainer) {
      starContainer.addEventListener('mouseleave', () => {
        const current = document.getElementById('ratingValue').value || 0;
        highlightStars(current);
      });
    }
  
    //submit
    const reviewFormElement = document.getElementById('reviewSubmissionForm');
    if (reviewFormElement) {
      reviewFormElement.addEventListener('submit', function(e) {
        const rating  = document.getElementById('ratingValue').value;
        const comment = document.querySelector('textarea[name="comment"]').value.trim();
  
        if (rating == 0) {
          alert('Please select a rating');
          e.preventDefault();
          return;
        }
        if (!comment) {
          alert('Please write a review');
          e.preventDefault();
          return;
        }
        console.log(`Submitting review: rating ${rating}, comment "${comment}"`);
      });
    }
  });