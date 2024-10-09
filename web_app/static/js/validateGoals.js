function validateForm() {
    const time = document.getElementById('time').value;
    const budget = document.getElementById('budget').value;
    const zipCode = document.getElementById('zipCode').value;
    const timeErrorMessage = document.getElementById('timeErrorMessage');
    const budgetErrorMessage = document.getElementById('budgetErrorMessage');
    const zipCodeErrorMessage = document.getElementById('zipCodeErrorMessage');

    if ( !/^\d+$/.test(time) || parseInt(time) <= 0) {
        timeErrorMessage.textContent = "Please enter a valid amount of time";
        return false;  // Prevent form submission
    }
    timeErrorMessage.textContent = "";
    if (!/^\d+(\.\d+)?$/.test(budget) || parseFloat(budget) <= 0){
      budgetErrorMessage.textContent = "Please enter a valid dollar amount";
      return false;
    }
    budgetErrorMessage.textContent = "";
    if (!/^\d{5,5}$/.test(zipCode) && !zipCode == ""){
      zipCodeErrorMessage.textContent = "Please enter a valid ZIP code";
      return false;
    }

    return true;  // Allow form submission
}