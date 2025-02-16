function redirectToLogin() {
    window.location.href = "/login";  
}

function signupUser() {
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const college = document.querySelector('select[name="college"]').value;
    
   
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password,
            college: college
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/login";  
        } else {
            alert("Signup failed: " + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}
