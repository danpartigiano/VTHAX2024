// static/js/main.js

function getUserLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                callback(latitude, longitude);
            },
            function(error) {
                alert('Unable to retrieve your location. Please allow location access.');
                console.error(error);
                callback(null, null);
            }
        );
    } else {
        alert('Geolocation is not supported by your browser.');
        callback(null, null);
    }
}

document.getElementById('find-organic-btn').addEventListener('click', function() {
    getUserLocation(function(latitude, longitude) {
        if (latitude && longitude) {
            // Show preferences section
            document.getElementById('preferences-section').style.display = 'block';

            // Handle form submission
            document.getElementById('preferences-form').addEventListener('submit', function(event) {
                event.preventDefault();
                const preferences = document.getElementById('preferences').value;

                // Fetch recommendations
                fetch('/get-organic-locations', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        latitude: latitude,
                        longitude: longitude,
                        preferences: preferences
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok.');
                    }
                    return response.text();
                })
                .then(html => {
                    // Display recommendations
                    document.body.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        } else {
            alert('Unable to retrieve your location.');
        }
    });
});

// Chatbot functionality (if implemented)
