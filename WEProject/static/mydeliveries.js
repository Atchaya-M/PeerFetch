document.addEventListener("DOMContentLoaded", () => {
    // Navigation links
    const navLinks = {
        myaccount: '/myaccount',
        order: '/order',
        myorders: '/myorders',
        deliver: '/deliver',
        ratings: '/ratings',
        homepage: '/homepage'
    };

    Object.keys(navLinks).forEach(id => {
        const link = document.getElementById(id);
        if (link) {
            link.addEventListener('click', () => {
                window.location.href = navLinks[id];
            });
        }
    });

    // Parse items from dataset and display
    document.querySelectorAll(".items-container").forEach(container => {
        try {
            const items = JSON.parse(container.dataset.items.replace(/'/g, '"'));
            items.forEach(item => {
                const li = document.createElement("li");
                li.innerHTML = `
                    <span class="item-name">${item.name}</span> :
                    <span class="item-quantity">${item.quantity} pcs</span> x
                    <span class="item-price">₹${item.price}</span>
                `;
                container.appendChild(li);
            });
        } catch (error) {
            console.error("Error parsing items:", error);
            container.textContent = "Failed to load items.";
        }
    });

    // Price calculations with delivery fee
    document.querySelectorAll("#total-price, #item-price").forEach(container => {
        const rawPrice = parseFloat(container.getAttribute('data-price'));
        if (isNaN(rawPrice)) {
            console.error("Invalid price value: ", rawPrice);
            return;
        }

        const updatedPrice = rawPrice < 30 ? rawPrice + 5 : rawPrice * 1.2;
        const deliveryFee = (updatedPrice - rawPrice).toFixed(2);

        container.innerHTML = `
            <li><span class="delivery-fee"><strong>Delivery Fee:</strong> ₹${deliveryFee}</span></li>
            <li><span class="updated-price"><strong>Total Price:</strong> ₹${updatedPrice.toFixed(2)}</span></li>
        `;
    });

    // Search function for filtering deliveries
    const searchBar = document.getElementById('search-bar');
    if (searchBar) {
        searchBar.addEventListener('input', () => {
            const query = searchBar.value.toLowerCase();
            document.querySelectorAll('.delivery-card').forEach(delivery => {
                const isMatch = Array.from(delivery.querySelectorAll('*')).some(field => 
                    field.textContent.toLowerCase().includes(query)
                );
                delivery.style.display = isMatch ? '' : 'none';
            });
        });
    }

    // Delivery status change logic
    document.querySelectorAll('.change-status-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const deliveryId = btn.getAttribute('data-delivery-id');
            const statusElement = btn.closest('.delivery-card').querySelector('.status');
            const currentStatus = statusElement.textContent.trim();

            if (confirm("Do you want to change status?")) {
                if (currentStatus === 'Accepted') {
                    updateStatus(deliveryId, 'Picked Up', btn);
                } else if (currentStatus === 'Picked Up') {
                    const otp = prompt("Enter OTP to change status to Delivered");
                    if (otp) {
                        verifyOtpAndUpdateStatus(deliveryId, otp, btn);
                    }
                }
            }
        });
    });
});

// Function to update status without reloading
function updateStatus(deliveryId, newStatus, button) {
    fetch(`/update_status/${deliveryId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ delivery_id: deliveryId, new_status: newStatus }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const statusElement = document.querySelector(`[data-delivery-id="${deliveryId}"]`).closest('.delivery-card').querySelector('.status');
            statusElement.textContent = newStatus;

            // Update button text dynamically
            if (newStatus === 'Picked Up') {
                button.textContent = 'Deliver';
            } else {
                button.style.display = 'none'; // Hide button after final status
            }
        } else {
            alert('Error changing status: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while changing the status.');
    });
}

// Function to verify OTP and update status
function verifyOtpAndUpdateStatus(deliveryId, otp, button) {
    fetch(`/update_status/${deliveryId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ delivery_id: deliveryId, otp: otp, new_status: 'Delivered' }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Status updated to Delivered');
            const statusElement = document.querySelector(`[data-delivery-id="${deliveryId}"]`).closest('.delivery-card').querySelector('.status');
            statusElement.textContent = 'Delivered';
            button.style.display = 'none';
        } else {
            alert('Invalid OTP');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while changing the status.');
    });
}
