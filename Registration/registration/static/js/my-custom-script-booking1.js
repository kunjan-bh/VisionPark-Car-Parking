document.addEventListener('DOMContentLoaded', function() {
    
    
    document.getElementById('location').addEventListener('change', function() {
        const selectedLocation = this.value;
        const slotsSection = document.getElementById('slots');
        const timeFieldsSection = document.getElementById('timeFields');
        if (selectedLocation === "Maitidevi-Sunway") {
            slotsSection.style.display = 'block';
        } else {
            slotsSection.style.display = 'none';
            timeFieldsSection.style.display = 'none';
            alert('No slots available at the moment for the selected location.');
        }
    });
    const slotButtons = document.querySelectorAll('.slot-btn');


    slotButtons.forEach(button => {
        button.addEventListener('click', function() {
          
            document.getElementById('selected_slot').value = this.getAttribute('data-slot');

            slotButtons.forEach(btn => btn.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
    // Handle slot selection
    document.getElementById('slots').addEventListener('click', function(event) {
        if (event.target && event.target.matches('.slot-btn')) {
            const slotButtons = document.querySelectorAll('.slot-btn');
            slotButtons.forEach(button => button.classList.remove('selected'));
            event.target.classList.add('selected');
            document.getElementById('timeFields').style.display = 'block';
        }
    });
    const hoursDisplay = document.getElementById('hours');
    const minutesDisplay = document.getElementById('minutes');
    const startTimeInput = document.getElementById('startTime');

    let currentTime = new Date();
    let real_hours = currentTime.getHours();
    let hours = currentTime.getHours();
    let minutes = Math.ceil(currentTime.getMinutes() / 10) * 10; // Round up to nearest 10 minutes

    // Ensure minutes are within bounds
    if (minutes === 60) {
        minutes = 0;
        hours = (hours + 1) % 24;
    }

    function updateDisplay() {
        hoursDisplay.textContent = String(hours).padStart(2, '0');
        minutesDisplay.textContent = String(minutes).padStart(2, '0');
        startTimeInput.value = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
    }

    function increaseHours() {
        hours = (hours + 1) % 24;
        updateDisplay();
    }

    function decreaseHours() {
        hours = (hours - 1 + 24) % 24;
        updateDisplay();
    }

    function increaseMinutes() {
        minutes = (minutes + 10) % 60;
        if (minutes === 0) { // Handle hour rollover
            increaseHours();
        }
        updateDisplay();
    }

    function decreaseMinutes() {
        minutes = (minutes - 10 + 60) % 60;
        if (minutes === 50) { // Handle hour rollover
            decreaseHours();
        }
        updateDisplay();
    }

    function validateTime() {
        const now = new Date();
        const selectedTime = new Date();
        selectedTime.setHours(hours, minutes);

        if (selectedTime < now) {
            alert('Selected time cannot be in the past. Please choose a future time.');
            // Reset to the current time
            hours = now.getHours();
            minutes = Math.ceil(now.getMinutes() / 10) * 10;
            if (minutes === 60) {
                minutes = 0;
                hours = (hours + 1) % 24;
            }
            updateDisplay();
        }
    }

    document.getElementById('hoursUp').addEventListener('click', function() {
        increaseHours();
        validateTime();
    });
    document.getElementById('hoursDown').addEventListener('click', function() {
        decreaseHours();
        validateTime();
    });
    document.getElementById('minutesUp').addEventListener('click', function() {
        increaseMinutes();
        validateTime();
    });
    document.getElementById('minutesDown').addEventListener('click', function() {
        decreaseMinutes();
        validateTime();
    });

    // Initialize display
    updateDisplay();
    
});
