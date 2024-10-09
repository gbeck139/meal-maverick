document.addEventListener('DOMContentLoaded', function() { 
// JavaScript to handle progress bar updates
            const mealForm = document.getElementById('mealForm');
            const progressBar = document.getElementById('progressBar');
            const budgetElement = document.getElementById("budget");
            const maxValue = parseFloat(budgetElement.getAttribute("data-budget"));

        mealForm.addEventListener('change', function() {
            let totalValue = 0;

            // Calculate total value of selected meals based on servings
            const mealsChecked = document.querySelectorAll('input[name="selected_meals"]:checked');
            mealsChecked.forEach(meal => {
                
              const id = meal.value;
              // const id = meal.id    
              const unitPriceValue = parseFloat(meal.getAttribute("data-price"));
              const servingsId = 'servings'+id; // Get the corresponding servings input ID
              const servings = parseInt(document.getElementById(servingsId).value); // Get the number of servings
                
                totalValue += unitPriceValue * servings; // Multiply price by servings
              console.log("change")
            });

            // Assume maximum value for progress is $100 (can be adjusted)
            const percentage = (totalValue / maxValue) * 100;

            // Update progress bar
            progressBar.style.width = percentage + '%';
            progressBar.textContent = "100%"//Math.round(percentage) + '%'; // Show percentage text
          console.log("loaded")
        });
   });