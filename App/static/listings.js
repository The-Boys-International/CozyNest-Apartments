document.addEventListener('DOMContentLoaded', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
    const rentButtons = document.querySelectorAll('.rent-button');
    rentButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        const apartmentId = this.getAttribute('href').split('=')[1];
        console.log(`Renting apartment ${apartmentId}`);
      });
    });
  });
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  const sidebarOverlay = document.querySelector('.sidebar-overlay');
  const closeSidebar = document.querySelector('.close-sidebar');
  const body = document.body;
  
  sidebarToggle.addEventListener('click', () => {
    body.classList.add('sidebar-active');
  });
  
  closeSidebar.addEventListener('click', () => {
    body.classList.remove('sidebar-active');
  });
  
  sidebarOverlay.addEventListener('click', () => {
    body.classList.remove('sidebar-active');
  });
  

  function filterListings() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const priceFilter = document.getElementById('priceFilter').value;
    const amenityCheckboxes = document.querySelectorAll('.amenity-filter:checked');
    const selectedAmenities = Array.from(amenityCheckboxes).map(cb => cb.value);
    
    document.querySelectorAll('.apartment-card').forEach(card => {
        const address = card.querySelector('.card-title').textContent.toLowerCase();
        const city = card.querySelector('.card-location').textContent.toLowerCase();
        const priceText = card.querySelector('.card-price').textContent.toLowerCase();
        const price = parseFloat(priceText.replace(/[^\d.]/g, '')); // Extract numeric price
        const amenities = Array.from(card.querySelectorAll('.card-amenities span')).map(span => span.textContent);
        
        // Search filter - matches any part of address, city, or price
        const matchesSearch = 
            address.includes(searchInput) || 
            city.includes(searchInput) ||
            priceText.includes(searchInput);
        
        // Price filter
        let matchesPrice = true;
        if (priceFilter) {
            if (priceFilter === '0-2000') matchesPrice = price < 2000;
            else if (priceFilter === '2000-3000') matchesPrice = price >= 2000 && price < 3000;
            else if (priceFilter === '3000-4000') matchesPrice = price >= 3000 && price < 4000;
            else if (priceFilter === '4000+') matchesPrice = price >= 4000;
        }
        
        // Amenities filter
        const matchesAmenities = selectedAmenities.length === 0 || 
            selectedAmenities.every(amenity => 
                amenities.some(a => a.toLowerCase().includes(amenity.toLowerCase()))
            );
        
        // Confirm filtering
        if (matchesSearch && matchesPrice && matchesAmenities) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Initialize event listeners for real-time filtering
document.addEventListener('DOMContentLoaded', () => {
    // Search input responds to typing
    document.getElementById('searchInput').addEventListener('input', filterListings);
    
    // Price filter responds to changes
    document.getElementById('priceFilter').addEventListener('change', filterListings);
    
    // Amenity checkboxes respond immediately
    document.querySelectorAll('.amenity-filter').forEach(checkbox => {
        checkbox.addEventListener('change', filterListings);
    });
    
    // Initialize sidebar functionality
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const closeSidebar = document.querySelector('.close-sidebar');
    const body = document.body;

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            body.classList.add('sidebar-active');
        });
    }

    if (closeSidebar) {
        closeSidebar.addEventListener('click', () => {
            body.classList.remove('sidebar-active');
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', () => {
            body.classList.remove('sidebar-active');
        });
    }
});