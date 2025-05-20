// Order form submission
const orderForm = document.getElementById("orderForm")

// Mock showNotification function (since it's not provided)
function showNotification(message) {
  alert(message) // Replace with a more sophisticated notification system if needed
}

if (orderForm) {
  orderForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // In a real application, you would send the form data to a server
    // For demo purposes, we'll just show a notification
    showNotification("Buyurtmangiz muvaffaqiyatli qabul qilindi!")

    // Reset form
    orderForm.reset()

    // Add the new order to the table (for demo purposes)
    const recentOrdersTable = document.getElementById("recentOrdersTable")
    if (recentOrdersTable) {
      const serviceType = document.getElementById("serviceType")
      const date = document.getElementById("date")

      const newRow = document.createElement("tr")
      newRow.innerHTML = `
                <td>1004</td>
                <td>${serviceType.options[serviceType.selectedIndex].text}</td>
                <td>${formatDate(date.value)}</td>
                <td><span class="status pending">Kutilmoqda</span></td>
                <td>-</td>
                <td>-</td>
            `

      recentOrdersTable.prepend(newRow)
    }
  })
}

// Format date for display
function formatDate(dateString) {
  const date = new Date(dateString)
  return `${date.getDate().toString().padStart(2, "0")}.${(date.getMonth() + 1).toString().padStart(2, "0")}.${date.getFullYear()}`
}

// Set user name in header
const userNameHeader = document.getElementById("userNameHeader")
const userName = document.getElementById("userName")

if (userNameHeader && userName) {
  // In a real application, you would get the user's name from the server
  // For demo purposes, we'll use a hardcoded name
  const demoUserName = "Aziz Rahimov"
  userNameHeader.textContent = demoUserName
  userName.textContent = demoUserName
}
