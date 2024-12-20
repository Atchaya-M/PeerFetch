
document.addEventListener("DOMContentLoaded", () => {

    const myaccountLink = document.getElementById('myaccount');
    const orderLink = document.getElementById('order');
    const myordersLink = document.getElementById('myorders');
    const deliverLink = document.getElementById('deliver');
    const ratingLink = document.getElementById('ratings');
    const homeLink = document.getElementById('homepage');


    myaccountLink.addEventListener('click', () => {
        window.location.href = '/myaccount';
       
    });

    orderLink.addEventListener('click', () => {
        window.location.href = '/order';
      
    });

    myordersLink.addEventListener('click', () => {
        window.location.href = '/myorders';
       
    });

    ratingLink.addEventListener('click', () => {
        window.location.href = '/ratings';
       
    });

    deliverLink.addEventListener('click', () => {
        window.location.href = 'deliver';
      
    });

    homeLink.addEventListener('click', () => {
        window.location.href = 'homepage';
      
    });

    const itemsContainers = document.querySelectorAll(".items-container");

    itemsContainers.forEach(container => {
        const rawItems = container.dataset.items;
    
        try {
            const formattedItems = rawItems.replace(/'/g, '"');
            const items = JSON.parse(formattedItems);
    
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

    const priceContainers = document.querySelectorAll("#total-price, #item-price");

    priceContainers.forEach(container => {
        const rawPrice = parseFloat(container.getAttribute('data-price'));
    
        if (isNaN(rawPrice)) {
            console.error("Invalid price value: ", rawPrice);
            return;
        }
    
        let updatedPrice;
        if (rawPrice < 30) {
            updatedPrice = rawPrice + 5;
        } else {
            updatedPrice = rawPrice * 1.2;
        }
    
        updatedPrice = updatedPrice.toFixed(2);
    
        const deliveryFee = (updatedPrice - rawPrice).toFixed(2);
        const deliveryLi = document.createElement("li");
        deliveryLi.innerHTML = `
            <span class="delivery-fee"><strong>Delivery Fee:</strong> ₹${deliveryFee}</span>
        `;
        
        const li = document.createElement("li");
        li.innerHTML = `
            <span class="updated-price"><strong>Total Price:</strong> ₹${updatedPrice}</span>
        `;
    
        container.appendChild(deliveryLi);
        container.appendChild(li);
    });

    const searchBar = document.getElementById('search-bar');
const deliveries = Array.from(document.querySelectorAll('.delivery-card'));

searchBar.addEventListener('input', () => {
    const query = searchBar.value.toLowerCase();

    deliveries.forEach(delivery => {
        const fields = Array.from(delivery.querySelectorAll('*')); 
        const isMatch = fields.some(field => field.textContent.toLowerCase().includes(query));

        if (isMatch) {
            delivery.style.display = ''; 
        } else {
            delivery.style.display = 'none';
        }
    });
});


});



//otp 
document.addEventListener('DOMContentLoaded', function() {
    const changeStatusBtns = document.querySelectorAll('.change-status-btn');

    changeStatusBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const deliveryId = btn.getAttribute('data-delivery-id');
            const currentStatus = btn.closest('.delivery-card').querySelector('.status').textContent.trim();

            // Prompt user to confirm status change
            if (confirm("Do you want to change status?")) {
                if (currentStatus === 'Accepted') {
                    // Change status to 'Picked Up'
                    updateStatus(deliveryId, 'Picked Up');
                } else if (currentStatus === 'Picked Up') {
                    // OTP verification for 'Delivered'
                    const otp = prompt("Enter OTP to change status to Delivered");
                    if (otp) {
                        verifyOtpAndUpdateStatus(deliveryId, otp);
                    }
                }
            }
        });
    });
});

function updateStatus(deliveryId, newStatus) {
    fetch(`/update_status/${deliveryId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ delivery_id: deliveryId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the status displayed in the UI
            const statusElement = document.querySelector(`[data-delivery-id="${deliveryId}"]`).closest('.delivery-card').querySelector('.status');
            statusElement.textContent = data.new_status;
        } else {
            alert('Error changing status: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while changing the status.');
    });
}

function verifyOtpAndUpdateStatus(deliveryId, otp) {
    fetch(`/update_status/${deliveryId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ otp: otp }), // Ensure OTP is sent correctly
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Status updated to Delivered');
            // Update the status in the UI
            const statusElement = document.querySelector(`[data-delivery-id="${deliveryId}"]`).closest('.delivery-card').querySelector('.status');
            statusElement.textContent = data.new_status;
        } else {
            alert('Invalid OTP');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while changing the status.');
    });
}
