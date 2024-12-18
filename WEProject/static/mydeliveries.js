
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