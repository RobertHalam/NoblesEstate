function toggleMenu() {
    let menu = document.getElementById("sliding-menu");
    if (menu.classList.contains("active")) {
        menu.classList.remove("active");
    } else {
        menu.classList.add("active");
    }
}

function validateForm() {
    let name = document.getElementById("contact-name").value.trim();
    let email = document.getElementById("contact-email").value.trim();
    let message = document.getElementById("contact-message").value.trim();

    if (name === "" || email === "" || message === "") {
        alert("All fields are required!");
        return false;
    }

    alert("Your message has been sent successfully!");
    return true;
}

