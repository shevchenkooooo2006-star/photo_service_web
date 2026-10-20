document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");
    const loginLink = document.getElementById("login-link");
    const logoutLink = document.getElementById("logout-link");
    if (token) {
        loginLink.classList.add("d-none");
        logoutLink.classList.remove("d-none");
        logoutLink.addEventListener("click", (e) => {
            e.preventDefault();
            localStorage.removeItem("access_token");
            window.location.href = "/";
        });
    }
});