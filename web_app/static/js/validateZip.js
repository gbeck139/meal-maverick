function validateForm() {
    const zipCode = document.getElementById('zipCode').value;
    const zipCodeErrorMessage = document.getElementById('zipCodeErrorMessage');

    if (!/^\d{5,5}$/.test(zipCode) && !zipCode == ""){
      zipCodeErrorMessage.textContent = "Please enter a valid ZIP code";
      return false;
    }

    return true;  // Allow form submission
}