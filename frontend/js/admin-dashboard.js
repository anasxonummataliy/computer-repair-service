import { Chart } from "@/components/ui/chart"
// Initialize charts
document.addEventListener("DOMContentLoaded", () => {
  const regionChartCanvas = document.getElementById("regionChart")
  const servicesChartCanvas = document.getElementById("servicesChart")

  if (regionChartCanvas) {
    const regionChart = new Chart(regionChartCanvas, {
      type: "bar",
      data: {
        labels: ["Sergeli", "Chilonzor", "Yunusobod", "Mirzo Ulug'bek", "Yakkasaroy", "Shayxontohur"],
        datasets: [
          {
            label: "Buyurtmalar soni",
            data: [65, 59, 80, 81, 56, 55],
            backgroundColor: "rgba(79, 70, 229, 0.8)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    })
  }

  if (servicesChartCanvas) {
    const servicesChart = new Chart(servicesChartCanvas, {
      type: "pie",
      data: {
        labels: ["Uy ta'mirlash", "Elektr xizmatlari", "Santexnika", "Tozalash", "Yuk tashish", "Kompyuter ta'mirlash"],
        datasets: [
          {
            data: [120, 90, 70, 85, 50, 60],
            backgroundColor: [
              "rgba(79, 70, 229, 0.8)",
              "rgba(16, 185, 129, 0.8)",
              "rgba(245, 158, 11, 0.8)",
              "rgba(239, 68, 68, 0.8)",
              "rgba(59, 130, 246, 0.8)",
              "rgba(139, 92, 246, 0.8)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    })
  }
})

// Show notification function
function showNotification(message) {
  alert(message) // Replace with a more sophisticated notification system if needed
}

// Message actions
const replyButtons = document.querySelectorAll(".btn-reply")
const markReadButtons = document.querySelectorAll(".btn-mark-read")

if (replyButtons.length > 0) {
  replyButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // In a real application, you would open a reply form
      // For demo purposes, we'll just show a notification
      showNotification("Javob berish oynasi ochilmoqda...")
    })
  })
}

if (markReadButtons.length > 0) {
  markReadButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // In a real application, you would update the message status on the server
      // For demo purposes, we'll just update the UI
      const messageCard = button.closest(".message-card")
      const statusElement = messageCard.querySelector(".message-status")

      statusElement.textContent = "O'qilgan"
      statusElement.classList.remove("new")
      statusElement.classList.add("read")

      button.remove()

      showNotification("Xabar o'qildi deb belgilandi")
    })
  })
}

// Set admin name in header
const adminName = document.getElementById("adminName")

if (adminName) {
  // In a real application, you would get the admin's name from the server
  // For demo purposes, we'll use a hardcoded name
  adminName.textContent = "Admin"
}
