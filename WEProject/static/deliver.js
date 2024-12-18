
document.querySelectorAll('.deliver-btn').forEach(button => {
    button.addEventListener('click', (event) => {
        const orderCard = event.target.closest('.order-card');
        const orderId = orderCard.querySelector('.order-id').textContent.split(':')[1].trim();
        
        if (confirm(`Are you sure you want to deliver Order ID: ${orderId}?`)) {
            alert(`Order ID: ${orderId} is now being delivered by you`);
            orderCard.style.opacity = '0.5';
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {

    const myaccountLink = document.getElementById('myaccount');
    const orderLink = document.getElementById('order');
    const mydeliverLink = document.getElementById('mydeliveries');
    const myordersLink = document.getElementById('myorders');
    const ratingLink = document.getElementById('ratings');
    const homeLink = document.getElementById('homepage');


    myaccountLink.addEventListener('click', () => {
        window.location.href = '/myaccount';
       
    });

    orderLink.addEventListener('click', () => {
        window.location.href = '/order';
      
    });

    mydeliverLink.addEventListener('click', () => {
        window.location.href = '/mydeliveries';
       
    });

    ratingLink.addEventListener('click', () => {
        window.location.href = '/ratings';
       
    });

    myordersLink.addEventListener('click', () => {
        window.location.href = 'myorders';
      
    });

    homeLink.addEventListener('click', () => {
        window.location.href = 'homepage';
      
    });

 

    document.querySelectorAll('.deliver-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            const orderId = event.target.getAttribute('data-order-id'); 
            
    
            fetch('/move_to_delivery', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ order_id: orderId }) 
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                 
                    window.location.href = "/mydeliveries";
                } else {
                    alert('Failed to move the order to delivery.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while moving the order to delivery.');
            });
        });
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
const orderCards = Array.from(document.querySelectorAll('.order-card'));

searchBar.addEventListener('input', () => {
    const query = searchBar.value.toLowerCase();

    orderCards.forEach(orderCard => {
    
        const fields = Array.from(orderCard.querySelectorAll('*'))
                            .map(field => field.textContent.toLowerCase());


        const isMatch = fields.some(field => field.includes(query));

        if (isMatch) {
            orderCard.style.display = ''; 
        } else {
            orderCard.style.display = 'none';
        }
    });
});

});



