// Global variables
let currentUser = null

// Initialize page
document.addEventListener("DOMContentLoaded", () => {
    // Load user data
    const userData = localStorage.getItem("user")
    if (userData) {
        currentUser = JSON.parse(userData)
    }

    // Initialize mobile menu
    initializeMobileMenu()

    // Initialize modals
    initializeModals()

    // Check authentication for dashboard pages
    if (window.location.pathname.includes("dashboard") && !currentUser) {
        window.location.href = "login.html"
    }
})

// Mobile menu functionality
function initializeMobileMenu() {
    const mobileMenuBtn = document.querySelector(".mobile-menu-btn")
    const sidebar = document.querySelector(".sidebar")

    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener("click", () => {
            sidebar.classList.toggle("open")
        })

        // Close menu when clicking outside
        document.addEventListener("click", (e) => {
            if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                sidebar.classList.remove("open")
            }
        })
    }
}

// Modal functionality
function initializeModals() {
    // Close modal when clicking outside
    window.addEventListener("click", (e) => {
        if (e.target.classList.contains("modal")) {
            closeModal(e.target)
        }
    })

    // Close modal with Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            const activeModal = document.querySelector(".modal.active")
            if (activeModal) {
                closeModal(activeModal)
            }
        }
    })
}

// Request modal functions
function openRequestModal() {
    const modal = document.getElementById("requestModal")
    if (modal) {
        modal.classList.add("active")
        modal.style.display = "flex"
    }
}

function closeRequestModal() {
    const modal = document.getElementById("requestModal")
    if (modal) {
        modal.classList.remove("active")
        modal.style.display = "none"
    }
}

function closeModal(modal) {
    modal.classList.remove("active")
    modal.style.display = "none"
}

// Form submission handlers
function handleRequestSubmit(event) {
    event.preventDefault()

    // Simulate form submission
    const submitBtn = event.target.querySelector('button[type="submit"]')
    const originalText = submitBtn.innerHTML

    submitBtn.innerHTML = '<span class="spinner"></span> Yuborilmoqda...'
    submitBtn.disabled = true

    setTimeout(() => {
        alert("Ta'mir so'rovingiz muvaffaqiyatli yuborildi!")
        submitBtn.innerHTML = originalText
        submitBtn.disabled = false
        closeRequestModal()
        event.target.reset()
    }, 2000)
}

// Authentication functions
function logout() {
    localStorage.removeItem("user")
    window.location.href = "index.html"
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString)
    return date.toLocaleDateString("uz-UZ")
}

function showNotification(message, type = "success") {
    const notification = document.createElement("div")
    notification.className = `notification ${type}`
    notification.textContent = message

    document.body.appendChild(notification)

    setTimeout(() => {
        notification.classList.add("show")
    }, 100)

    setTimeout(() => {
        notification.classList.remove("show")
        setTimeout(() => {
            document.body.removeChild(notification)
        }, 300)
    }, 3000)
}

// Dashboard specific functions
function updateTaskStatus(taskId, newStatus) {
    showNotification(`Vazifa ${taskId} holati "${newStatus}" ga o'zgartirildi`)
}

function assignMaster(requestId) {
    showNotification(`So'rov ${requestId} uchun master tayinlanmoqda`)
}

// Search and filter functions
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId)
    const table = document.getElementById(tableId)

    if (!input || !table) return

    input.addEventListener("keyup", function () {
        const filter = this.value.toLowerCase()
        const rows = table.getElementsByTagName("tr")

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i]
            const cells = row.getElementsByTagName("td")
            let found = false

            for (let j = 0; j < cells.length; j++) {
                if (cells[j].textContent.toLowerCase().includes(filter)) {
                    found = true
                    break
                }
            }

            row.style.display = found ? "" : "none"
        }
    })
}

// Initialize search functionality
document.addEventListener("DOMContentLoaded", () => {
    searchTable("searchInput", "dataTable")
})

// Add spinner CSS for loading states
const spinnerCSS = `
.spinner {
    display: inline-block;
    width: 12px;
    height: 12px;
    border: 2px solid #ffffff;
    border-radius: 50%;
    border-top-color: transparent;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 24px;
    border-radius: 6px;
    color: white;
    font-weight: 500;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    z-index: 1000;
}

.notification.success {
    background-color: #10b981;
}

.notification.error {
    background-color: #ef4444;
}

.notification.show {
    transform: translateX(0);
}
`

// Add spinner styles to head
const style = document.createElement("style")
style.textContent = spinnerCSS
document.head.appendChild(style)

// Book modal functions
function openBookModal() {
    const modal = document.getElementById("bookModal")
    if (modal) {
        modal.classList.add("active")
        modal.style.display = "flex"
        document.body.style.overflow = "hidden" // Scroll ni bloklash
    }
}

function closeBookModal() {
    const modal = document.getElementById("bookModal")
    if (modal) {
        modal.classList.remove("active")
        modal.style.display = "none"
        document.body.style.overflow = "" // Scroll ni qayta yoqish
    }
}

// Close modal when clicking outside
window.onclick = (event) => {
    const modal = document.getElementById("bookModal")
    if (event.target === modal) {
        closeBookModal()
    }
}

// Form submission
document.getElementById("bookForm").addEventListener("submit", function (e) {
    e.preventDefault()

    const submitBtn = this.querySelector('button[type="submit"]')
    const originalText = submitBtn.textContent

    // Show loading state
    submitBtn.innerHTML = '<span class="spinner"></span> Yuborilmoqda...'
    submitBtn.disabled = true

    // Simulate form submission
    setTimeout(() => {
        // Show success message
        submitBtn.innerHTML = "✓ Muvaffaqiyatli yuborildi!"
        submitBtn.style.background = "#16a34a"

        // Reset form and close modal after 2 seconds
        setTimeout(() => {
            this.reset()
            closeBookModal()
            submitBtn.innerHTML = originalText
            submitBtn.style.background = ""
            submitBtn.disabled = false
        }, 2000)
    }, 2000)
})

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault()
        const target = document.querySelector(this.getAttribute("href"))
        if (target) {
            target.scrollIntoView({
                behavior: "smooth",
                block: "start",
            })
        }
    })
})

// Mobile menu toggle function
function toggleMobileMenu() {
    const nav = document.querySelector("nav")
    const hamburger = document.querySelector(".hamburger")

    nav.classList.toggle("active")
    hamburger.classList.toggle("active")

    // Prevent body scroll when menu is open
    if (nav.classList.contains("active")) {
        document.body.style.overflow = "hidden"
    } else {
        document.body.style.overflow = ""
    }
}

// Close mobile menu when clicking on nav links
document.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
        const nav = document.querySelector("nav")
        const hamburger = document.querySelector(".hamburger")

        nav.classList.remove("active")
        hamburger.classList.remove("active")
        document.body.style.overflow = ""
    })
})

// Close mobile menu when clicking outside
document.addEventListener("click", (e) => {
    const nav = document.querySelector("nav")
    const hamburger = document.querySelector(".hamburger")

    if (!nav.contains(e.target) && !hamburger.contains(e.target)) {
        nav.classList.remove("active")
        hamburger.classList.remove("active")
        document.body.style.overflow = ""
    }
})

// Mobile menu toggle
const hamburger = document.querySelector(".hamburger")
const navLinks = document.querySelector(".nav-links")

if (hamburger) {
    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("active")
        hamburger.classList.toggle("active")
    })
}

// Active navigation link highlighting
window.addEventListener("scroll", () => {
    const sections = document.querySelectorAll("section[id]")
    const navLinks = document.querySelectorAll(".nav-links a")

    let current = ""
    sections.forEach((section) => {
        const sectionTop = section.offsetTop
        const sectionHeight = section.clientHeight
        if (scrollY >= sectionTop - 200) {
            current = section.getAttribute("id")
        }
    })

    navLinks.forEach((link) => {
        link.classList.remove("active")
        if (link.getAttribute("href") === `#${current}`) {
            link.classList.add("active")
        }
    })
})

// Form validation and animations
document.addEventListener("DOMContentLoaded", () => {
    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px",
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("fade-in")
            }
        })
    }, observerOptions)

    // Observe elements for animation
    document.querySelectorAll(".service-card, .advantage-card, .contact-item").forEach((el) => {
        observer.observe(el)
    })
})
