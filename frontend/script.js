console.log("Dashboard is loaded");

const dashboard = document.getElementById("dashboard");

function loadPage(page) {
    dashboard.innerHTML="";

    const content = document.createElement("div");
    content.className = "data-card";

    if (page === "Home") {
        content.innerHTML = "<h2>Home</h2><p>This is the home page.</p>";
    } else if (page === "United States") {
        content.innerHTML = "<h2>United States</h2><p>This is where US data goes.</p>";
    } else if (page === "United Kingdom") {
        content.innerHTML = "<h2>United Kingdom</h2><p>This is where UK data goes.</p>";
    } else if (page === "Europe") {
        content.innerHTML = "<h2>Europe</h2><p>This is where EU data goes.</p>";
    }

    dashboard.appendChild(content);
}

const navButtons = document.querySelectorAll(".nav-button");
navButtons.forEach(button => {
    button.addEventListener("click", () => {
        const page = button.dataset.page;
        loadPage(page);
    });
});

loadPage("Home")