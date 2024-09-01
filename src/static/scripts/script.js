// toggle dark-light
document.addEventListener('DOMContentLoaded', () => {
  const toggleButton = document.getElementById('checkbox');
  
  // Load the saved theme or default to light mode
  const currentTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', currentTheme);

  // Toggle theme on button click
  toggleButton.addEventListener('click', () => {
    const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });
});

// Menu
const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom in a channel mesage thread
const conversationThread = document.querySelector(".channel__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;