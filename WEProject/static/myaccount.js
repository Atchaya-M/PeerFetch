document.addEventListener("DOMContentLoaded", function() {

    const deliverLink = document.getElementById('deliver');
    const orderLink = document.getElementById('order');
    const mydeliverLink = document.getElementById('mydeliveries');
    const myordersLink = document.getElementById('myorders');
    const ratingLink = document.getElementById('ratings');
    const homeLink = document.getElementById('homepage');


    deliverLink.addEventListener('click', () => {
        window.location.href = '/deliver';
       
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

    const changePasswordBtn = document.getElementById("change-password-btn");
    const viewOrdersBtn = document.getElementById("view-orders-btn");
    const viewDeliveriesBtn = document.getElementById("view-deliveries-btn");


    document.getElementById("change-password-btn").addEventListener("click", function() {
        const currentPassword = prompt("Enter your current password:");
        
       
        if (currentPassword) {
            
            fetch('/check-current-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ current_password: currentPassword })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
             
                    const newPassword = prompt("Enter your new password:");
    
                    if (newPassword) {
                       
                        fetch('/change-password', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                current_password: currentPassword,
                                new_password: newPassword
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert("Password changed successfully!");
                            } else {
                                alert(data.message);  
                            }
                        });
                    } else {
                        alert("New password cannot be empty.");
                    }
                } else {
                    alert(data.message);  
                }
            });
        } else {
            alert("Current password is required.");
        }
    });
    

  
    viewOrdersBtn.addEventListener("click", function() {
        const ordersList = document.getElementById("orders-list");
       
        ordersList.innerHTML = "<li>Order #1 - Item A</li><li>Order #2 - Item B</li>";
        alert("Orders fetched successfully!");
    });

  
    viewDeliveriesBtn.addEventListener("click", function() {
        const deliveriesList = document.getElementById("deliveries-list");
        deliveriesList.innerHTML = "<li>Delivery #1 - Address A</li><li>Delivery #2 - Address B</li>";
        alert("Deliveries fetched successfully!");
    });
});

document.getElementById("logout-btn").addEventListener("click", function() {
    window.location.href = "/logout";
});

