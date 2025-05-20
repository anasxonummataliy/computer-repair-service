import { Chart } from "@/components/ui/chart"
// Initialize charts
document.addEventListener("DOMContentLoaded", () => {
  const servicesChartCanvas = document.getElementById("servicesChart")

  if (servicesChartCanvas) {
    const servicesChart = new Chart(servicesChartCanvas, {
      type: "bar",
      data: {
        labels: ["Uy ta'mirlash", "Elektr xizmatlari", "Santexnika", "Tozalash", "Yuk tashish", "Kompyuter ta'mirlash"],
        datasets: [
          {
            label: "Buyurtmalar soni",
            data: [12, 19, 8, 15, 7, 6],
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
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    })
  }
})

// Modal functionality
const assignButtons = document.querySelectorAll(".btn-assign")
const assignMasterModal = document.getElementById("assignMasterModal")
const closeModalBtn = document.querySelector(".close")
const assignMasterForm = document.getElementById("assignMasterForm")

// Mock showNotification function for demonstration purposes
function showNotification(message) {
  alert(message) // Replace with a more sophisticated notification system if needed
}

if (assignButtons.length > 0 && assignMasterModal) {
  assignButtons.forEach((button) => {
    button.addEventListener("click", () => {
      assignMasterModal.classList.add("show")
    })
  })

  closeModalBtn.addEventListener("click", () => {
    assignMasterModal.classList.remove("show")
  })

  window.addEventListener("click", (e) => {
    if (e.target === assignMasterModal) {
      assignMasterModal.classList.remove("show")
    }
  })

  assignMasterForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // In a real application, you would send the form data to a server
    // For demo purposes, we'll just show a notification and close the modal
    showNotification("Master muvaffaqiyatli tayinlandi!")
    assignMasterModal.classList.remove("show")

    // Update the table (for demo purposes)
    const masterSelect = document.getElementById("masterSelect")
    const selectedMaster = masterSelect.options[masterSelect.selectedIndex].text

    // Find the first row with "Kutilmoqda" status and update it
    const pendingRows = document.querySelectorAll(".status.pending")
    if (pendingRows.length > 0) {
      const row = pendingRows[0].closest("tr")
      row.cells[3].innerHTML = '<span class="status in-progress">Jarayonda</span>'
      row.cells[4].textContent = selectedMaster

      // Replace assign button with view button
      const actionCell = row.cells[row.cells.length - 1]
      actionCell.innerHTML = '<button class="btn-view">Ko\'rish</button>'
    }
  })
}

// Set company name in header
const companyNameHeader = document.getElementById("companyNameHeader")
const companyName = document.getElementById("companyName")

if (companyNameHeader && companyName) {
  // In a real application, you would get the company's name from the server
  // For demo purposes, we'll use a hardcoded name
  const demoCompanyName = "TechServe LLC"
  companyNameHeader.textContent = demoCompanyName
  companyName.textContent = demoCompanyName
}
