document.addEventListener('DOMContentLoaded', function() {

  const signoutBtn = document.getElementById('signout-btn');
  if (signoutBtn) {
      signoutBtn.addEventListener('click', function() {
          alert('Sign out functionality would go here');
      });
  }

 
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const previewGrid = document.getElementById('file-preview');
  let files = [];

 
  dropzone.addEventListener('click', function() {
      fileInput.click();
  });


  fileInput.addEventListener('change', function(e) {
      files = Array.from(e.target.files);
      renderPreviews();
  });


  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, unhighlight, false);
  });

  function highlight() {
      dropzone.classList.add('active');
  }

  function unhighlight() {
      dropzone.classList.remove('active');
  }

  dropzone.addEventListener('drop', function(e) {
      const dt = e.dataTransfer;
      files = Array.from(dt.files);
      renderPreviews();
  });

  function renderPreviews() {
      previewGrid.innerHTML = '';
      
      if (files.length === 0) {
          return;
      }

      files.forEach((file, index) => {
          if (!file.type.match('image.*')) return;

          const reader = new FileReader();
          reader.onload = function(e) {
              const previewItem = document.createElement('div');
              previewItem.className = 'preview-item';
              
              const img = document.createElement('img');
              img.src = e.target.result;
              
              const removeBtn = document.createElement('button');
              removeBtn.className = 'remove-btn';
              removeBtn.innerHTML = '×';
              removeBtn.addEventListener('click', function(e) {
                  e.stopPropagation();
                  files.splice(index, 1);
                  renderPreviews();
              });

              previewItem.appendChild(img);
              previewItem.appendChild(removeBtn);
              previewGrid.appendChild(previewItem);
          };
          reader.readAsDataURL(file);
      });
  }

  // Form submission
  const form = document.getElementById('listing-form');
  if (form) {
      form.addEventListener('submit', function(e) {
          e.preventDefault();
          
          const formData = new FormData(form);
          
          // amenities
          const amenities = [];
          document.querySelectorAll('input[name="amenities"]:checked').forEach(checkbox => {
              amenities.push(checkbox.value);
          });
          formData.append('amenities', amenities.join(', '));
          
          // files
          files.forEach(file => {
              formData.append('images', file);
          });
          
          console.log('Form data to submit:', {
              address: formData.get('address'),
              price: formData.get('price'),
              occupants: formData.get('occupants'),
              amenities: formData.get('amenities'),
              fileCount: files.length
          });
          
          form.reset();
          files = [];
          renderPreviews();
      });
  }
});

document.addEventListener('DOMContentLoaded', function() {

  //submitting files
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const previewGrid = document.getElementById('file-preview');
  let files = [];

  dropzone.addEventListener('click', function(e) {
    e.preventDefault();
    fileInput.click();
  });

  fileInput.addEventListener('change', function(e) {
    files = Array.from(e.target.files);
    renderPreviews();
  });

  dropzone.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropzone.classList.add('active');
  });

  dropzone.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropzone.classList.remove('active');
  });

  dropzone.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropzone.classList.remove('active');
    
    const dt = e.dataTransfer;
    files = Array.from(dt.files).filter(file => 
      file.type.match('image.*') && 
      ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'].includes(file.type)
    );
    
    if (files.length === 0) {
      alert('Please upload only image files (PNG, JPG, JPEG, GIF, or WEBP)');
      return;
    }
    
    renderPreviews();
  });

  function renderPreviews() {
    previewGrid.innerHTML = '';
    
    if (files.length === 0) {
      return;
    }

    files.forEach((file, index) => {
      const reader = new FileReader();
      reader.onload = function(e) {
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';
        
        const img = document.createElement('img');
        img.src = e.target.result;
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-btn';
        removeBtn.innerHTML = '×';
        removeBtn.addEventListener('click', function(e) {
          e.stopPropagation();
          files.splice(index, 1);
          renderPreviews();
        });

        previewItem.appendChild(img);
        previewItem.appendChild(removeBtn);
        previewGrid.appendChild(previewItem);
      };
      reader.readAsDataURL(file);
    });
  }
});