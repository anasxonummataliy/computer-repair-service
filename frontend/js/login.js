// Login form submission
const loginForm = document.getElementById("loginForm")

// Function to display notifications (assumed to be defined elsewhere or imported)
// For demonstration purposes, we'll define a simple one here.
function showNotification(message) {
  alert(message) // Replace with a more sophisticated notification system if needed
}

if (loginForm) {
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault()

    const email = document.getElementById("email").value

    // In a real application, you would validate credentials on the server
    // For demo purposes, we'll just show a notification and redirect based on email
    showNotification("Tizimga muvaffaqiyatli kirdingiz!")

    // Simulate redirect based on user type (for demo purposes)
    setTimeout(() => {
      if (email.includes("admin")) {
        window.location.href = "admin-dashboard.html"
      } else if (email.includes("business")) {
        window.location.href = "business-dashboard.html"
      } else {
        window.location.href = "user-dashboard.html"
      }
    }, 2000)
  })
}
