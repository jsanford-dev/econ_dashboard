const dashboard = document.getElementById("dashboard");
const homeButton = document.getElementById("home-button");
const dropdownToggle = document.querySelector(".dropdown-toggle");
const dropdown = document.querySelector(".dropdown");
const countryItems = document.querySelectorAll(".dropdown-item");

function loadHome() {
    dashboard.innerHTML = `
        <div class='data-card'>
            <h2>Welcome to the Macro Dashboard</h2>
            <p>Select a country to view macroeconomic data</p>
        </div>
    `;
}

function loadCountry(countryCode) {
    dashboard.innerHTML = `
        <div class='data-card'>
            <h2>${countryCode.replace("-", "").toUpperCase()}</h2>
            <p>Display data for ${countryCode.replace("-", "")}</p>
        </div>
    `;
}

// Toggle dropdown open/close
dropdownToggle.addEventListener("click", () => {
    dropdown.classList.toggle("open");
});

// Home button loads home content
homeButton.addEventListener("click", () => {
    loadHome();
});

// Country buttons load specific country content
countryItems.forEach(item => {
    item.addEventListener("click", () => {
        const selectedCountry = item.dataset.country;
        dropdown.classList.remove("open");
        loadCountry(selectedCountry);
    });
});

// Initial load
loadHome();