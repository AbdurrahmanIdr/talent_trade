document.addEventListener("DOMContentLoaded", function() {

    const menuButton = document.querySelector('#menuButton');
    const navLinks = document.querySelector('header nav');

    if(menuButton) {
        menuButton.addEventListener('click', function() {
            navLinks.classList.toggle('open');
        });
    }
});
