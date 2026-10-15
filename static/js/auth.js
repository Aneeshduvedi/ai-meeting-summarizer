
document.addEventListener("DOMContentLoaded", function () {
    // Show or hide the password
    document.querySelectorAll("[data-password-toggle]").forEach(function (button) {
        button.addEventListener("click", function () {
            const wrapper = button.closest(".auth-password-wrap");
            const passwordInput = wrapper?.querySelector("input");

            if (!passwordInput) return;

            const showPassword = passwordInput.type === "password";
            passwordInput.type = showPassword ? "text" : "password";

            button.textContent = showPassword ? "Hide" : "Show";
            button.setAttribute("aria-label", showPassword ? "Hide password" : "Show password");
            button.setAttribute("aria-pressed", String(showPassword));
        });
    });

    // Provide feedback when the login form is submitted
    document.querySelectorAll("[data-auth-form]").forEach(function (form) {
        form.addEventListener("submit", function () {
            const submitButton = form.querySelector('button[type="submit"]');

            if (submitButton && form.checkValidity()) {
                submitButton.disabled = true;
                submitButton.textContent =
                    submitButton.dataset.loadingText || "Please wait...";
            }
        });
    });
});
