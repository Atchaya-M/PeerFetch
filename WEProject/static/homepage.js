
document.addEventListener('DOMContentLoaded', () => {
    const myaccountLink = document.getElementById('myaccount');
    const orderLink = document.getElementById('order');
    const mydeliverLink = document.getElementById('mydeliveries');
    const myordersLink = document.getElementById('myorders');
    const ratingLink = document.getElementById('ratings');
    const deliverLink = document.getElementById('deliver');


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

    deliverLink.addEventListener('click', () => {
        window.location.href = 'deliver';
      
    });
});
