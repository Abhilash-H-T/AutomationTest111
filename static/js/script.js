// static/js/script.js

function showSection(sectionId) {
    var sections = document.getElementsByClassName('section-content');
    for (var i = 0; i < sections.length; i++) {
        if (sections[i]) {
            sections[i].style.display = 'none';
        }
    }
    var targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
    } else {
        console.warn(`No element found with ID: ${sectionId}`);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var currentPage = document.body.getAttribute('data-page'); // Use a data attribute to identify the page
    if (currentPage) {
        showSection(currentPage);
    }
});
