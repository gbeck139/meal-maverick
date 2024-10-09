        // JavaScript to handle progress bar updates
        const mealForm = document.getElementById('mealForm');
        const progressBar = document.getElementById('progressBar');

        mealForm.addEventListener('change', function() {
            let totalValue = 0;

            // Calculate total value of selected meals based on servings
            const mealsChecked = document.querySelectorAll('input[name="selected_meals"]:checked');
            mealsChecked.forEach(meal => {
                
              const [id, unitPrice] = meal.value.split(',');
              // const id = meal.id    
              const unitPriceValue = parseFloat(unitPrice);
              const servingsId = 'servings'+id; // Get the corresponding servings input ID
              const servings = parseInt(document.getElementById(servingsId).value); // Get the number of servings
                
                totalValue += unitPriceValue * servings; // Multiply price by servings
            });

            // Assume maximum value for progress is $100 (can be adjusted)
            const maxValue = ;
            const percentage = (totalValue / maxValue) * 100;

            // Update progress bar
            progressBar.style.width = percentage + '%';
            progressBar.textContent = Math.round(percentage) + '%'; // Show percentage text
        });