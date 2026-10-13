
document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile sidebar toggle
    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menuToggle");

    if (sidebar && menuToggle) {
        menuToggle.addEventListener("click", () => {
            const isOpen = sidebar.classList.toggle("is-open");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });

        // Close sidebar when clicking outside it on mobile
        document.addEventListener("click", (event) => {
            if (
                window.innerWidth <= 768 &&
                sidebar.classList.contains("is-open") &&
                !sidebar.contains(event.target) &&
                !menuToggle.contains(event.target)
            ) {
                sidebar.classList.remove("is-open");
                menuToggle.setAttribute("aria-expanded", "false");
            }
        });

        // Close sidebar after selecting a navigation link
        sidebar.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                sidebar.classList.remove("is-open");
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    // 2. Toast notifications
    window.showToast = (message, type = "info") => {
        const container = document.getElementById("toastContainer");

        if (!container || !message) {
            return;
        }

        const allowedTypes = ["success", "danger", "warning", "info"];

        if (!allowedTypes.includes(type)) {
            type = "info";
        }

        const toast = document.createElement("div");
        toast.className =
            `toast align-items-center text-bg-${type} border-0`;
        toast.setAttribute("role", "status");
        toast.setAttribute("aria-live", "polite");
        toast.setAttribute("aria-atomic", "true");

        const row = document.createElement("div");
        row.className = "d-flex";

        const body = document.createElement("div");
        body.className = "toast-body";
        body.textContent = message;

        const closeButton = document.createElement("button");
        closeButton.type = "button";
        closeButton.className =
            "btn-close btn-close-white me-2 m-auto";
        closeButton.setAttribute("aria-label", "Close");

        row.append(body, closeButton);
        toast.appendChild(row);
        container.appendChild(toast);

        if (window.bootstrap && window.bootstrap.Toast) {
            const toastInstance = new bootstrap.Toast(toast, {
                delay: 3500
            });

            closeButton.addEventListener("click", () => {
                toastInstance.hide();
            });

            toast.addEventListener("hidden.bs.toast", () => {
                toast.remove();
            });

            toastInstance.show();
        } else {
            // Fallback if Bootstrap JavaScript is unavailable
            toast.classList.add("show");

            closeButton.addEventListener("click", () => {
                toast.remove();
            });
        }
    };

    // 3. Display Django messages as toast notifications
    const messageContainer = document.getElementById("djangoMessages");

    if (messageContainer) {
        messageContainer.querySelectorAll(".alert").forEach((alert) => {
            const message = alert.textContent
                .replace("×", "")
                .trim();

            let type = "info";

            if (alert.classList.contains("alert-success")) {
                type = "success";
            } else if (
                alert.classList.contains("alert-error") ||
                alert.classList.contains("alert-danger")
            ) {
                type = "danger";
            } else if (alert.classList.contains("alert-warning")) {
                type = "warning";
            }

            if (message) {
                window.showToast(message, type);
            }
        });

        messageContainer.remove();
    }

    // 4. Confirm before deleting a meeting
    document.querySelectorAll("form").forEach((form) => {
        const action = form.getAttribute("action") || "";

        if (action.includes("/delete/")) {
            // Remove existing inline confirmation to prevent duplicate dialogs
            form.removeAttribute("onsubmit");

            form.addEventListener("submit", (event) => {
                const confirmed = window.confirm(
                    "Are you sure you want to delete this meeting and its report? This action cannot be undone."
                );

                if (!confirmed) {
                    event.preventDefault();
                    event.stopImmediatePropagation();
                }
            });
        }
    });

    // 5. Loading feedback and duplicate submission prevention
    document.querySelectorAll("form").forEach((form) => {
        // Do not change search or filter form buttons
        if (
            form.querySelector('input[type="date"]') ||
            form.querySelector('select[name="sort"]') ||
            form.querySelector('input[name="q"]')
        ) {
            return;
        }

        form.addEventListener("submit", (event) => {
            // Respect HTML form validation
            if (!form.checkValidity()) {
                return;
            }

            const action = form.getAttribute("action") || "";

            // Delete forms have their own confirmation and remain unchanged
            if (action.includes("/delete/")) {
                return;
            }

            // Prevent duplicate submissions
            if (form.dataset.submitting === "true") {
                event.preventDefault();
                return;
            }

            const button = form.querySelector(
                'button[type="submit"], input[type="submit"]'
            );

            if (!button || button.disabled) {
                return;
            }

            form.dataset.submitting = "true";
            button.disabled = true;

            if (button.tagName === "BUTTON") {
                button.dataset.originalText = button.textContent.trim();
                button.textContent = "Please wait...";
            } else {
                button.dataset.originalValue = button.value;
                button.value = "Please wait...";
            }
        });
    });
});
