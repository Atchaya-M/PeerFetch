

document.addEventListener("DOMContentLoaded", function() {

    const myaccountLink = document.getElementById('myaccount');
    const deliverLink = document.getElementById('deliver');
    const mydeliverLink = document.getElementById('mydeliveries');
    const myordersLink = document.getElementById('myorders');
    const ratingLink = document.getElementById('ratings');
    const homeLink = document.getElementById('homepage');


    myaccountLink.addEventListener('click', () => {
        window.location.href = '/myaccount';
       
    });

    deliverLink.addEventListener('click', () => {
        window.location.href = '/deliver';
      
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

    
    const items = document.querySelectorAll('.item');
    
    items.forEach(item => {
        const plusBtn = item.querySelector('.plus-btn');
        const minusBtn = item.querySelector('.minus-btn');
        const quantitySpan = item.querySelector('.quantity');
        const itemName = item.querySelector('h3').textContent;
        const priceText = Array.from(item.querySelectorAll('p'))
        .find(p => p.textContent.includes('Price:')).textContent.trim();
        const priceMatch = priceText.match(/Price:\s*₹\s*([\d.]+)/);
        const itemPrice = priceMatch ? parseFloat(priceMatch[1]) : 0;
        let quantity = 0;
        
        plusBtn.addEventListener('click', function() {
            quantity++;
            quantitySpan.textContent = quantity;
            updateItemInSelectedItems(itemName, itemPrice, quantity);
        });

        minusBtn.addEventListener('click', function() {
            if (quantity > 0) {
                quantity--;
                quantitySpan.textContent = quantity;
                updateItemInSelectedItems(itemName, itemPrice, quantity);
            }
        });
    });
});

let selectedItems = [];

function updateItemInSelectedItems(name, price, quantity) {
   
    let selectedItem = selectedItems.find(item => item.name === name);

    if (!selectedItem && quantity > 0) {
       
        selectedItems.push({ name, price, quantity });
    } else if (selectedItem) {
        
        selectedItem.quantity = quantity;
    }
    
    updateSelectedItems();
    updateTotalPrice();
    localStorage.setItem("selectedItems", JSON.stringify(selectedItems));
    localStorage.setItem("totalPrice", calculateTotalPrice());
}

function calculateTotalPrice() {
    let totalPrice = 0;
    selectedItems.forEach(item => {
        totalPrice += item.price * item.quantity;
    });
    
    return totalPrice.toFixed(2);
}

function updateSelectedItems() {
    const selectedItemsList = document.getElementById('selected-items-list');
    const totalPriceElement = document.getElementById('total-price');
    selectedItemsList.innerHTML = ''; 

    let totalPrice = 0;
    
    selectedItems.forEach(item => {
        if (item.quantity > 0) {
            const listItem = document.createElement('li');
            listItem.textContent = `${item.name} - ${item.quantity} x ₹${item.price.toFixed(2)}`;
            selectedItemsList.appendChild(listItem);
            totalPrice += item.price * item.quantity;
        }
    });

    totalPriceElement.textContent = totalPrice.toFixed(2);
}

// items and total are swapped
function updateTotalPrice() {
    const totalPriceElement = document.getElementById('items-price');
    const itemsPriceElement = document.getElementById('total-price');
    
    let itemsPrice = parseFloat(itemsPriceElement.textContent);

  
    let totalPrice;
    if (itemsPrice < 30) {
        totalPrice = itemsPrice + 5;  
    } else {
        totalPrice = itemsPrice * 1.2;  
    }
    totalPrice = Math.round(totalPrice);
    if (itemsPrice == 0){
        totalPrice = 0;
    }
  
    totalPriceElement.textContent = totalPrice.toFixed(2);  
}




document.getElementById("place-order").addEventListener("click", function () {
    const selectedItems = JSON.parse(localStorage.getItem("selectedItems")) || [];
    const totalPrice = parseFloat(localStorage.getItem("totalPrice") || "0.00");
    const location = document.getElementById("location").value;
    const comments = document.getElementById("comments").value;

    const orderDetails = {
        selectedItems: selectedItems,
        totalPrice: totalPrice,
        location: location,
        comments: comments
    };

 
    fetch("/order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(orderDetails),
    })
    .then((response) => {
        if (response.ok && totalPrice > 0) {
            alert("Order placed successfully!");
            window.location.href = "/myorders"; 
        } else {
            alert("Failed to place order. Please try again.");
        }
    })
    .catch((error) => console.error("Error:", error));
});

