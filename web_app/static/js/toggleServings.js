    function toggleServings(mealId) {
        const servings = document.getElementById('servings' + mealId);
        const checkbox = document.getElementById('meal' + mealId);
        
        // Toggle the display of the servings input based on the checkbox state
        if (checkbox.checked) {
            servings.style.display = 'inline'; // Show servings input
            servings.textContent = " servings";
        } else {
            servings.style.display = 'none'; // Hide servings input
            servings.textContent = "";
        }
    }