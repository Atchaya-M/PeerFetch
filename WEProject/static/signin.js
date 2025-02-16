


document.querySelector('.login').addEventListener('click', async (event) => {
    event.preventDefault(); 

    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const college = document.querySelector('select[name="college"]').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password, college }),
        });

        const result = await response.json();

        if (result.success) {
            window.location.href = "/homepage";  
        } else {
            alert(result.message || "Invalid credentials");  
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
});

function loginUser() {
    document.querySelector('.login').click();
}

function redirectToSignup() {
    window.location.href = '/signup';
}

