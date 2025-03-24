document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('download-btn');
    const videoUrlInput = document.getElementById('video-url');
    const platformSelect = document.getElementById('platform');
    const statusDiv = document.getElementById('status');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const statusMessage = document.getElementById('status-message');
    const errorMessage = document.getElementById('error-message');
    const downloadLink = document.getElementById('download-link');
    
    downloadBtn.addEventListener('click', function() {
        const url = videoUrlInput.value.trim();
        const platform = platformSelect.value;
        
        if (!url) {
            showError('Please enter a video URL');
            return;
        }
        
        // Reset UI
        hideError();
        hideResult();
        showStatus('Downloading video...');
        
        // Send request to backend
        fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                platform: platform
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                showResult(data.download_url, data.filename);
            }
        })
        .catch(error => {
            showError('An error occurred while downloading the video');
            console.error('Error:', error);
        });
    });
    
    function showStatus(message) {
        statusMessage.textContent = message;
        statusDiv.classList.remove('hidden');
    }
    
    function hideStatus() {
        statusDiv.classList.add('hidden');
    }
    
    function showResult(downloadUrl, filename) {
        hideStatus();
        downloadLink.href = downloadUrl;
        downloadLink.download = filename;
        resultDiv.classList.remove('hidden');
    }
    
    function hideResult() {
        resultDiv.classList.add('hidden');
    }
    
    function showError(message) {
        hideStatus();
        errorMessage.textContent = message;
        errorDiv.classList.remove('hidden');
    }
    
    function hideError() {
        errorDiv.classList.add('hidden');
    }
});