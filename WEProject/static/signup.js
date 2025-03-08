function redirectToLogin() {
    window.location.href = "/login";  
}

document.addEventListener("DOMContentLoaded", function () {
    const termsModal = document.getElementById("termsModal");   // ✅ Get modal
    const termsOverlay = document.getElementById("termsOverlay"); // ✅ Get overlay
    const signUpBtn = document.getElementById("signUpBtn");  // ✅ Get Sign Up button
    const acceptBtn = document.getElementById("acceptTerms");  // ✅ Get Accept button
    const cancelBtn = document.getElementById("cancelTerms");  // ✅ Get Cancel button

    // ✅ Ensure the Sign-Up button shows the terms modal
    signUpBtn.addEventListener("click", function (event) {
        event.preventDefault();
        console.log("Sign-Up button clicked, opening terms modal...");
        termsModal.style.display = "block";
        termsOverlay.style.display = "block";
    });

    // ✅ Accept button should close modal and trigger signup
    acceptBtn.addEventListener("click", function () {
        console.log("Accept clicked, closing modal and signing up...");
        termsModal.style.display = "none";
        termsOverlay.style.display = "none";
        signupUser();  // ✅ Calls signup function
    });

    // ✅ Cancel button should close the modal only
    cancelBtn.addEventListener("click", function () {
        console.log("Cancel clicked, closing modal...");
        termsModal.style.display = "none";
        termsOverlay.style.display = "none";
    });

    // ✅ Clicking outside the modal should also close it
    termsOverlay.addEventListener("click", function () {
        console.log("Clicked outside modal, closing...");
        termsModal.style.display = "none";
        termsOverlay.style.display = "none";
    });
});

// ✅ Function for user signup (No changes here)
function signupUser() {
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const college = document.querySelector('select[name="college"]').value;

    console.log("Signing up user:", email, college); // ✅ Debugging log

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
            console.log("Signup successful, redirecting...");
            window.location.href = "/login";  // ✅ Redirect on success
        } else {
            alert("Signup failed: " + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}


// function signupUser() {
//     const email = document.querySelector('input[name="email"]').value;
//     const password = document.querySelector('input[name="password"]').value;
//     const college = document.querySelector('select[name="college"]').value;
    
//     fetch('/signup', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             email: email,
//             password: password,
//             college: college
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             window.location.href = "/login";  
//         } else {
//             alert("Signup failed: " + data.message);
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }
