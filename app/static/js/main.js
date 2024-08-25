document.addEventListener("DOMContentLoaded", function() {
    // Your JavaScript code goes here

    // Example: Toggle mobile menu
    const menuButton = document.querySelector('#menuButton');
    const navLinks = document.querySelector('header nav');

    if(menuButton) {
        menuButton.addEventListener('click', function() {
            navLinks.classList.toggle('open');
        });
    }
});
