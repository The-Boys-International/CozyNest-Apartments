
document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('apartmentVideo');
    
    // For mobile devices, we need to play the video programmatically
    video.play().catch(error => {
        // Autoplay was prevented, show fallback image
        console.log('Video autoplay prevented:', error);
        const videoContainer = document.querySelector('.video-background');
        videoContainer.innerHTML = '<div class="fallback-image"></div>';
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

