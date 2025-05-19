document.addEventListener("DOMContentLoaded", () => {
    // Login Form Submission
    const loginForm = document.getElementById("loginForm")
    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            e.preventDefault()

            const formData = {
                email: document.getElementById("email").value,
                password: document.getElementById("password").value,
                remember: document.getElementById("remember")?.checked || false,
            }

            // Send login request to server (will be implemented with FastAPI)
            login(formData)
                .then((response) => {
                    // Store user data in localStorage
                    localStorage.setItem("user", JSON.stringify(response.user))
                    localStorage.setItem("token", response.token)

                    // Redirect based on user role
                    redirectBasedOnRole(response.user.role)
                })
                .catch((error) => {
                    alert("Login xatolik. Email yoki parol noto'g'ri.")
                    console.error("Error:", error)
                })
        })
    }

    // Register Form Submission
    const registerForm = document.getElementById("registerForm")
    if (registerForm) {
        // Show/hide business fields based on user type
        const userTypeSelect = document.getElementById("userType")
        const businessFields = document.getElementById("businessFields")

        if (userTypeSelect && businessFields) {
            userTypeSelect.addEventListener("change", function () {
                if (this.value === "business") {
                    businessFields.classList.remove("hidden")
                } else {
                    businessFields.classList.add("hidden")
                }
            })
        }

        registerForm.addEventListener("submit", (e) => {
            e.preventDefault()

            // Validate password match
            const password = document.getElementById("password").value
            const confirmPassword = document.getElementById("confirmPassword").value

            if (password !== confirmPassword) {
                alert("Parollar mos kelmadi!")
                return
            }

            const formData = {
                fullName: document.getElementById("fullName").value,
                email: document.getElementById("email").value,
                phone: document.getElementById("phone").value,
                userType: document.getElementById("userType").value,
                password: password,
            }

            // Add business fields if business user
            if (formData.userType === "business") {
                formData.companyName = document.getElementById("companyName").value
                formData.companyAddress = document.getElementById("companyAddress").value
            }

            // Send registration request to server (will be implemented with FastAPI)
            register(formData)
                .then((response) => {
                    alert("Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!")

                    // Store user data in localStorage
                    localStorage.setItem("user", JSON.stringify(response.user))
                    localStorage.setItem("token", response.token)

                    // Redirect based on user role
                    redirectBasedOnRole(response.user.role)
                })
                .catch((error) => {
                    alert("Ro'yxatdan o'tishda xatolik yuz berdi.")
                    console.error("Error:", error)
                })
        })
    }
})

// Function to login (will be connected to FastAPI)
async function login(formData) {
    // This is a placeholder function that will be replaced with actual API call
    // For now, we'll simulate a successful login based on email
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Simulate different user roles based on email
            let role = "regular"
            let userData = {
                id: 1,
                fullName: "Foydalanuvchi",
                email: formData.email,
                role: "regular",
            }

            if (formData.email.includes("admin")) {
                role = "admin"
                userData = {
                    id: 3,
                    fullName: "Admin Adminov",
                    email: formData.email,
                    role: "admin",
                }
            } else if (formData.email.includes("business")) {
                role = "business"
                userData = {
                    id: 2,
                    fullName: "Biznes Foydalanuvchi",
                    email: formData.email,
                    role: "business",
                    companyName: "ABC Kompaniyasi",
                    companyAddress: "Toshkent sh., Chilonzor tumani",
                }
            }

            resolve({
                success: true,
                user: userData,
                token: "sample_token_" + Math.random().toString(36).substr(2),
            })
        }, 1000)
    })
}

// Function to register (will be connected to FastAPI)
async function register(formData) {
    // This is a placeholder function that will be replaced with actual API call
    return new Promise((resolve) => {
        setTimeout(() => {
            const userData = {
                id: Math.floor(Math.random() * 1000) + 10,
                fullName: formData.fullName,
                email: formData.email,
                phone: formData.phone,
                role: formData.userType,
            }

            if (formData.userType === "business") {
                userData.companyName = formData.companyName
                userData.companyAddress = formData.companyAddress
            }

            resolve({
                success: true,
                user: userData,
                token: "sample_token_" + Math.random().toString(36).substr(2),
            })
        }, 1000)
    })
}

// Function to redirect based on user role
function redirectBasedOnRole(role) {
    switch (role) {
        case "admin":
            window.location.href = "admin-dashboard.html"
            break
        case "business":
            window.location.href = "business-dashboard.html"
            break
        default:
            window.location.href = "user-dashboard.html"
            break
    }
}

// Check if user is logged in
function checkAuth() {
    const token = localStorage.getItem("token")
    const user = JSON.parse(localStorage.getItem("user") || "{}")

    if (!token || !user.id) {
        window.location.href = "login.html"
        return null
    }

    return user
}

// Logout function
function logout() {
    localStorage.removeItem("token")
    localStorage.removeItem("user")
    window.location.href = "index.html"
}
  