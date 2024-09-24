

// Poll every 5 seconds

document.addEventListener('DOMContentLoaded', () => {
    // Your fetch function and other code here
    let lastLicensePlate = ''; // Store the last known license plate
    

    async function checkLicensePlateUpdate() {
        try {
            // Send a request to the server to get the current booking details for the logged-in user
            const response = await fetch('http://127.0.0.1:8000/get_latest_license_plate/', {
                method: 'GET',  // Assuming a GET request for fetching current booking details
            });
    
            if (!response.ok) {
                console.error('Network response was not ok:', response.statusText);
                return;
            }
    
            // Parse the response JSON data
            const data = await response.json();
            const currentLicensePlate = data.license_plate; // Assuming 'license_plate' is returned in the response
            const currentstatus = data.status; // Assuming 'license_plate' is returned in the response
    
            console.log('Current License Plate:', currentLicensePlate);
    
            // Compare the current license plate with the last known license plate
            if (currentstatus == 'ended'){
                window.location.href = "finish-session/";
            }
            if (currentLicensePlate !== lastLicensePlate) {
                console.log('License plate has been updated:', currentLicensePlate);
    
                // Update the last known license plate to the new value
                lastLicensePlate = currentLicensePlate;
                //hghghgh document.getElementById('licensePlate').textContent = currentLicensePlate;
                document.getElementById('license-plate').textContent = currentLicensePlate;
                // Perform an action when the license plate is updated, such as redirecting or displaying a message
                // window.location.href = "confirmation-image/"; // Redirect on update
            } else {
                console.log('No update in license plate.');
            }
            
        } catch (error) {
            console.error('Error fetching license plate updates:', error);
        }
    }
    setInterval(checkLicensePlateUpdate, 500);
});