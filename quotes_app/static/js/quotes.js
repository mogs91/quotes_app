// Rating functionality
function rateQuote(quoteId, rating) {
    fetch('/api/rate_quote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            quote_id: quoteId,
            rating: rating
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update UI
            const ratingElement = document.querySelector(`#quote-${quoteId} .rating-value`);
            if (ratingElement) {
                ratingElement.textContent = `Rating: ${data.new_rating}`;
            }
            
            // Update stars
            const stars = document.querySelectorAll(`#quote-${quoteId} .star`);
            stars.forEach((star, index) => {
                if (index < rating) {
                    star.classList.add('active');
                } else {
                    star.classList.remove('active');
                }
            });
            
            // Show success message
            showNotification('Rating saved!', 'success');
        } else {
            // Show error message
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to save rating. Please try again.', 'error');
    });
}

// Notification function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Fade in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Fade out and remove
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Social media sharing
function shareQuote(text, author) {
    const shareDropdown = event.currentTarget.nextElementSibling;

    if (shareDropdown.style.display === 'block') {
        shareDropdown.style.display = 'none';
    } else {
        // Close any open dropdowns
        document.querySelectorAll('.share-dropdown').forEach(dropdown => {
            dropdown.style.display = 'none';
        });

        shareDropdown.style.display = 'block';
    }

    // Close when clicking outside
    document.addEventListener('click', function closeDropdown(e) {
        if (!e.target.closest('.share-buttons')) {
            shareDropdown.style.display = 'none';
            document.removeEventListener('click', closeDropdown);
        }
    });

    // Prevent event from bubbling
    event.stopPropagation();
}

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Quote copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Could not copy text: ', err);
        showNotification('Failed to copy quote', 'error');
    });
}