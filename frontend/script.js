console.log("Dashboard is loaded!")

const dashboard = document.getElementById("dashboard");

function loadPage(page) {
    dashboard.innerHTML = "";

    const content = document.createElement("div");
    content.className = "data-card";

    if (page === "Home") {
        content.innerHTML = "<h2>Home</h2><p>This is the home page.</p>";
    } else if (page === "United States") {
        content.innerHTML = `
            <div class="card-header">
                <h2>United States</h2>
                <div class="sub-nav">
                    <button class="sub-button" data-subpage="Labour">Labour</button>
                    <button class="sub-button" data-subpage="Inflation">Inflation</button>
                    <button class="sub-button" data-subpage="Yields">Yields</button>
                </div>
            </div>
            <div id="us-dashboard-content">
                <p>Select a sub-category above to view data.</p>
            </div>
        `;

        // Attach event Listeners to sub-buttons
        content.querySelectorAll(".sub-button").forEach(button => {
            button.addEventListener("click", () => {
                const subpage = button.dataset.subpage;
                const subContent = content.querySelector("#us-dashboard-content");

                if (subpage === "Labour") {
                    subContent.innerHTML = `
                    <h3>Labour Statistics</h3>
                    <p>Unemployment rate, participation rate, etc.</p>
                    <img src="http://localhost:5000/chart/unemployment" alt="Unemployment Chart" style="max-width:100%; height:auto;">
                    `;
                } else if (subpage === "Inflation") {
                    subContent.innerHTML = "<h3>Inflation</h3><p>CPI, Core CPI, etc.</p>";
                } else if (subpage === "Yields") {
                    subContent.innerHTML = "<h3>Yields</h3><p>US Treasury Yields, curve data, etc.</p>";
                }
            });
        });

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

loadPage("Home");