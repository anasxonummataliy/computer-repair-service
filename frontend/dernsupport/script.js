document.addEventListener("DOMContentLoaded", () => {
  // Mobile Menu Toggle
  const hamburger = document.querySelector(".hamburger")
  const navLinks = document.querySelector(".nav-links")
  const authButtons = document.querySelector(".auth-buttons")

  if (hamburger) {
    hamburger.addEventListener("click", function () {
      this.classList.toggle("active")

      if (navLinks) {
        navLinks.classList.toggle("show")
      }

      if (authButtons) {
        authButtons.classList.toggle("show")
      }
    })
  }

  // Password Toggle
  const togglePassword = document.querySelectorAll(".toggle-password")

  togglePassword.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      const passwordInput = this.previousElementSibling

      if (passwordInput.type === "password") {
        passwordInput.type = "text"
        this.classList.remove("fa-eye-slash")
        this.classList.add("fa-eye")
      } else {
        passwordInput.type = "password"
        this.classList.remove("fa-eye")
        this.classList.add("fa-eye-slash")
      }
    })
  })

  // Form Validation
  const contactForm = document.getElementById("contactForm")
  const loginForm = document.getElementById("loginForm")
  const registerForm = document.getElementById("registerForm")
  const newOrderForm = document.getElementById("newOrderForm")
  const dashboardContactForm = document.getElementById("dashboardContactForm")

  // Contact Form Validation
  if (contactForm) {
    contactForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Simple validation
      const name = document.getElementById("name").value
      const email = document.getElementById("email").value
      const message = document.getElementById("message").value

      if (name && email && message) {
        // Show success message
        alert("Xabaringiz muvaffaqiyatli yuborildi!")
        contactForm.reset()
      } else {
        alert("Iltimos, barcha maydonlarni to'ldiring!")
      }
    })
  }

  // Login Form Validation
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const email = document.getElementById("login-email").value
      const password = document.getElementById("login-password").value

      if (email && password) {
        // Redirect to dashboard (for demo purposes)
        window.location.href = "user-dashboard.html"
      } else {
        alert("Iltimos, barcha maydonlarni to'ldiring!")
      }
    })
  }

  // Register Form Validation
  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const firstName = document.getElementById("first-name").value
      const lastName = document.getElementById("last-name").value
      const email = document.getElementById("register-email").value
      const password = document.getElementById("register-password").value
      const confirmPassword = document.getElementById("confirm-password").value
      const terms = document.getElementById("terms").checked

      if (firstName && lastName && email && password && confirmPassword && terms) {
        if (password !== confirmPassword) {
          alert("Parollar mos kelmadi!")
          return
        }

        // Redirect to dashboard (for demo purposes)
        window.location.href = "user-dashboard.html"
      } else {
        alert("Iltimos, barcha maydonlarni to'ldiring!")
      }
    })
  }

  // New Order Form Validation
  if (newOrderForm) {
    newOrderForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const serviceType = document.getElementById("service-type").value
      const problemDescription = document.getElementById("problem-description").value

      if (serviceType && problemDescription) {
        // Show success message
        alert("Buyurtmangiz muvaffaqiyatli qabul qilindi!")
        newOrderForm.reset()
      } else {
        alert("Iltimos, barcha majburiy maydonlarni to'ldiring!")
      }
    })
  }

  // Dashboard Contact Form Validation
  if (dashboardContactForm) {
    dashboardContactForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const recipient = document.getElementById("contact-recipient").value
      const subject = document.getElementById("contact-subject").value
      const message = document.getElementById("contact-message").value

      if (recipient && subject && message) {
        // Show success message
        alert("Xabaringiz muvaffaqiyatli yuborildi!")
        dashboardContactForm.reset()
      } else {
        alert("Iltimos, barcha maydonlarni to'ldiring!")
      }
    })
  }

  // Set current date in dashboard
  const currentDateElement = document.getElementById("current-date")
  if (currentDateElement) {
    const now = new Date()
    const options = { day: "numeric", month: "short", year: "numeric" }
    currentDateElement.textContent = now.toLocaleDateString("uz-UZ", options)
  }

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      if (this.getAttribute("href") !== "#") {
        e.preventDefault()

        const targetId = this.getAttribute("href")
        const targetElement = document.querySelector(targetId)

        if (targetElement) {
          window.scrollTo({
            top: targetElement.offsetTop - 70,
            behavior: "smooth",
          })
        }
      }
    })
  })
})
