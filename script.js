// File preview functionality
document.getElementById('file-upload').addEventListener('change', function(e) {
    let file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(event) {
            const fileType = file.type;
            
            if (fileType.startsWith('image')) {
                document.getElementById('preview-img').style.display = 'block';
                document.getElementById('preview-img').src = event.target.result;
                document.getElementById('preview-text').style.display = 'none';
            } else if (fileType === 'application/pdf') {
                document.getElementById('preview-img').style.display = 'none';
                document.getElementById('preview-text').style.display = 'block';
                document.getElementById('preview-text').textContent = 'PDF file selected: Preview not available.';
            }
        };
        
        reader.readAsDataURL(file);
    }
});

// Upload functionality
document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    let fileInput = document.getElementById('file-input');
    let formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Send the file via AJAX
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display result
        let resultDiv = document.getElementById('result');
        if (data.message) {
            resultDiv.textContent = data.message;
        } else {
            resultDiv.textContent = data.error || 'Error occurred';
        }
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        document.getElementById('result').textContent = 'An error occurred while processing the file.';
    });
});
