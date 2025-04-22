function toggleDropdown() {
    document.querySelector('.dropdown').classList.toggle('show');
  }

  // Close the dropdown when clicking outside
  window.onclick = function(e) {
    if (!e.target.matches('.dropdown-toggle')) {
      var dropdowns = document.getElementsByClassName("dropdown");
      for (var i = 0; i < dropdowns.length; i++) {
        dropdowns[i].classList.remove('show');
      }
    }
  }