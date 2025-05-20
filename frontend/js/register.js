// Show/hide business fields based on user type selection
const userTypeSelect = document.getElementById("userType")
const businessFields = document.getElementById("businessFields")
const registerForm = document.getElementById("registerForm")

// Mock showNotification function (replace with your actual implementation)
function showNotification(message) {
  alert(message) // Or use a more sophisticated notification system
}

if (userTypeSelect && businessFields) {
  userTypeSelect.addEventListener("change", () => {
    if (userTypeSelect.value === "business") {
      businessFields.classList.remove("hidden")
    } else {
      businessFields.classList.add("hidden")
    }
  })
}

// Form validation and submission
if (registerForm) {
  registerForm.addEventListener("submit", (e) => {
    e.preventDefault()

    const password = document.getElementById("password").value
    const confirmPassword = document.getElementById("confirmPassword").value

    if (password !== confirmPassword) {
      alert("Parollar mos kelmadi!")
      return
    }

    // In a real application, you would send the form data to a server
    // For demo purposes, we'll just show a notification and redirect
    showNotification("Ro'yxatdan muvaffaqiyatli o'tdingiz!")

    // Simulate redirect after registration
    setTimeout(() => {
      if (userTypeSelect.value === "business") {
        window.location.href = "business-dashboard.html"
      } else {
        window.location.href = "user-dashboard.html"
      }
    }, 2000)
  })
}
