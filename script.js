// Function to save suggestions to localStorage
function saveSuggestion(suggestion) {
    let suggestions = JSON.parse(localStorage.getItem('suggestions')) || [];
    suggestions.push(suggestion);
    localStorage.setItem('suggestions', JSON.stringify(suggestions));
}

// Function to display suggestions from localStorage
function displaySuggestions() {
    let suggestions = JSON.parse(localStorage.getItem('suggestions')) || [];
    const suggestionsList = document.getElementById('suggestions-list');
    suggestionsList.innerHTML = suggestions.length > 0 ? 
        suggestions.map(suggestion => `<p>${suggestion}</p>`).join('') :
        '<p>No suggestions yet.</p>';
}

// Event listener for the submit button
document.getElementById('submit-btn').addEventListener('click', function() {
    const suggestionText = document.getElementById('suggestion').value.trim();
    
    if (suggestionText) {
        saveSuggestion(suggestionText);
        document.getElementById('suggestion').value = '';  // Clear the input
        displaySuggestions();  // Update the list of suggestions
    } else {
        alert('Please enter a suggestion.');
    }
});

// Initialize the page with any saved suggestions
window.onload = displaySuggestions;
