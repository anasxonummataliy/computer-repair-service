// document.addEventListener('DOMContentLoaded', () => {
//     // Check if user is logged in
//     const user = checkAuth();
//     if (!user) return;

//     // Set user name in header and sidebar
//     const userNameElement = document.getElementById('userName');
//     const sidebarUserNameElement = document.getElementById('sidebarUserName');
//     const companyNameElement = document.getElementById('companyName');
//     const sidebarCompanyNameElement = document.getElementById('sidebarCompanyName');
//     const adminNameElement = document.getElementById('adminName');
//     const sidebarAdminNameElement = document.getElementById('sidebarAdminName');

//     if (userNameElement && sidebarUserNameElement && user.role === 'regular') {
//         userNameElement.textContent = user.fullName;
//         sidebarUserNameElement.textContent = user.fullName;
//     }

//     if (companyNameElement && sidebarCompanyNameElement && user.role === 'business') {
//         companyNameElement.textContent = user.companyName || 'Kompaniya';
//         sidebarCompanyNameElement.textContent = user.companyName || 'Kompaniya';
//     }

//     if (adminNameElement && sidebarAdminNameElement && user.role === 'admin') {
//         adminNameElement.textContent = user.fullName;
//         sidebarAdminNameElement.textContent = user.fullName;
//     }

//     // Sidebar navigation
//     const sidebarLinks = document.querySelectorAll('.sidebar-nav a[data-section]');
//     sidebarLinks.forEach(link => {
//         link.addEventListener('click', function (e) {
//             e.preventDefault();

//             // Remove active class from all links
//             sidebarLinks.forEach(l => l.parentElement.classList.remove('active'));

//             // Add active class to clicked link
//             this.parentElement.classList.add('active');

//             // Hide all sections
//             const sections = document.querySelectorAll('.dashboard-section');
//             sections.forEach(section => section.classList.remove('active'));

//             // Show selected section
//             const sectionId = this.getAttribute('data-section');
//             document.getElementById(sectionId).classList.add('active');
//         });
//     });

//     // Logout button
//     const logoutBtn = document.getElementById('logoutBtn');
//     const adminLogoutBtn = document.getElementById('adminLogoutBtn');

//     if (logoutBtn) {
//         logoutBtn.addEventListener('click', (e) => {
//             e.preventDefault();
//             logout();
//         });
//     }

//     if (adminLogoutBtn) {
//         adminLogoutBtn.addEventListener('click', (e) => {
//             e.preventDefault();
//             logout();
//         });
//     }

//     // Load user orders
//     const ordersList = document.getElementById('ordersList');
//     if (ordersList) {
//         loadUserOrders(ordersList);
//     }

//     // Order filters
//     const statusFilter = document.getElementById('statusFilter');
//     const dateFilter = document.getElementById('dateFilter');
//     const refreshOrders = document.getElementById('refreshOrders');

//     if (statusFilter && dateFilter && refreshOrders) {
//         statusFilter.addEventListener('change', function () {
//             loadUserOrders(ordersList, this.value, dateFilter.value);
//         });

//         dateFilter.addEventListener('change', function () {
//             loadUserOrders(ordersList, statusFilter.value, this.value);
//         });

//         refreshOrders.addEventListener('click', () => {
//             loadUserOrders(ordersList, statusFilter.value, dateFilter.value);
//         });
//     }

//     // New order form
//     const newOrderForm = document.getElementById('newOrderForm');
//     if (newOrderForm) {
//         newOrderForm.addEventListener('submit', (e) => {
//             e.preventDefault();

//             const formData = {
//                 serviceId: document.getElementById('serviceType').value,
//                 address: document.getElementById('orderAddress').value,
//                 date: document.getElementById('orderDate').value,
//                 time: document.getElementById('orderTime').value,
//                 description: document.getElementById('orderDescription').value,
//                 userId: user.id
//             };

//             // Send order to server (will be implemented with FastAPI)
//             createOrder(formData)
//                 .then(response => {
//                     alert('Buyurtma muvaffaqiyatli yuborildi!');
//                     newOrderForm.reset();

//                     // Switch to orders tab
//                     const ordersLink = document.querySelector('.sidebar-nav a[data-section="orders"]');
//                     if (ordersLink) {
//                         ordersLink.click();

//                         // Reload orders
//                         loadUserOrders(ordersList);
//                     }
//                 })
//                 .catch(error => {
//                     alert('Buyurtma yuborishda xatolik yuz berdi.');
//                     console.error('Error:', error);
//                 });
//         });
//     }

//     // Profile form
//     const profileForm = document.getElementById('profileForm');
//     if (profileForm) {
//         // Fill profile form with user data
//         document.getElementById('profileFullName').value = user.fullName || '';
//         document.getElementById('profileEmail').value = user.email || '';
//         document.getElementById('profilePhone').value = user.phone || '';
//         document.getElementById('profileAddress').value = user.address || '';

//         profileForm.addEventListener('submit', (e) => {
//             e.preventDefault();

//             // Validate password match if new password is provided
//             const newPassword = document.getElementById('newPassword').value;
//             const confirmNewPassword = document.getElementById('confirmNewPassword').value;

//             if (newPassword && newPassword !== confirmNewPassword) {
//                 alert('Yangi parollar mos kelmadi!');
//                 return;
//             }

//             const formData = {
//                 fullName: document.getElementById('profileFullName').value,
//                 email: document.getElementById('profileEmail').value,
//                 phone: document.getElementById('profilePhone').value,
//                 address: document.getElementById('profileAddress').value,
//                 currentPassword: document.getElementById('currentPassword').value,
//                 newPassword: newPassword
//             };

//             // Update profile (will be implemented with FastAPI)
//             updateProfile(formData)
//                 .then(response => {
//                     alert('Profil ma\'lumotlari muvaffaqiyatli yangilandi!');

//                     // Update user data in localStorage
//                     const updatedUser = { ...user, ...formData };
//                     delete updatedUser.currentPassword;
//                     delete updatedUser.newPassword;

//                     localStorage.setItem('user', JSON.stringify(updatedUser));

//                     // Clear password fields
//                     document.getElementById('currentPassword').value = '';
//                     document.getElementById('newPassword').value = '';
//                     document.getElementById('confirmNewPassword').value = '';

//                     // Update user name in header and sidebar
//                     if (userNameElement && sidebarUserNameElement) {
//                         userNameElement.textContent = form
  