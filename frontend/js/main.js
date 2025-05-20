// Toggle mobile menu
const menuToggle = document.querySelector(".menu-toggle")
const nav = document.querySelector("nav ul")

if (menuToggle) {
  menuToggle.addEventListener("click", () => {
    nav.classList.toggle("show")
  })
}

// User dropdown menu
const userInfo = document.querySelector(".user-info")
const dropdownMenu = document.querySelector(".dropdown-menu")

if (userInfo) {
  userInfo.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show")
  })

  // Close dropdown when clicking outside
  document.addEventListener("click", (e) => {
    if (!userInfo.contains(e.target) && !dropdownMenu.contains(e.target)) {
      dropdownMenu.classList.remove("show")
    }
  })
}

// Contact form submission
const contactForm = document.getElementById("contactForm")
const notification = document.getElementById("notification")

if (contactForm) {
  contactForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // In a real application, you would send the form data to a server
    // For demo purposes, we'll just show a notification
    showNotification("Xabaringiz muvaffaqiyatli yuborildi!")

    // Reset form
    contactForm.reset()
  })
}

// Show notification function
function showNotification(message) {
  if (notification) {
    notification.querySelector("p").textContent = message
    notification.classList.add("show")

    setTimeout(() => {
      notification.classList.remove("show")
    }, 3000)
  }
}

// Logout functionality
const logoutBtn = document.getElementById("logoutBtn")

if (logoutBtn) {
  logoutBtn.addEventListener("click", (e) => {
    e.preventDefault()

    // In a real application, you would handle logout on the server
    // For demo purposes, we'll just redirect to the login page
    window.location.href = "login.html"
  })
}

// Cabinet link functionality
const cabinetLink = document.getElementById("cabinetLink")

if (cabinetLink) {
  cabinetLink.addEventListener("click", (e) => {
    e.preventDefault()

    // In a real application, you would check the user's role and redirect accordingly
    // For demo purposes, we'll just show a notification
    showNotification("Shaxsiy kabinetga o'tish...")

    // Simulate redirect based on current page
    const currentPage = window.location.pathname

    if (currentPage.includes("user-dashboard")) {
      window.location.href = "business-dashboard.html"
    } else if (currentPage.includes("business-dashboard")) {
      window.location.href = "admin-dashboard.html"
    } else if (currentPage.includes("admin-dashboard")) {
      window.location.href = "user-dashboard.html"
    }
  })
}
