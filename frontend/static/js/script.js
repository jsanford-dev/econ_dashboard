const dashboard = document.getElementById("dashboard");
const homeButton = document.getElementById("home-button");
const dropdownToggle = document.querySelector(".dropdown-toggle");
const dropdown = document.querySelector(".dropdown");

// Deafult view
function loadHome() {
    dashboard.innerHTML = `
        <div class='data-card'>
            <h2>Welcome to the Macro Dashboard</h2>
            <p>Select a country to view macroeconomic data</p>
        </div>
    `;
}

// Load country home page
function loadCountryOverview(country) {
    const countryLabel = country.replace("-", " ").toUpperCase();

    dashboard.innerHTML = `
        <div class='data-card'>
            <h2>${countryLabel} Overview</h2>
            <p>This is the overview page for ${countryLabel}. You can select a topic like Labor, Inflation, or Yields to explore more data.</p>
        </div>
    `;
}

// Load country sub-topic
function loadCountryTopic(country, topic) {
    const countryLabel = country.replace("-", " ").toUpperCase();
    const topicLabel = topic.charAt(0).toUpperCase() + topic.slice(1);

    dashboard.innerHTML = `
    <div class='data-card'>
        <h2>${countryLabel} - ${topicLabel}</h2>
        <p>Loading data for ${topicLabel}...</p>
    </div>
`;

    // TODO: Add API call here
}

function renderTopicData(country, topic, data) {
    return `
        <div class='data-card'>
            <h2>${country} - ${topic}</h2>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        </div>
    `;
}
// Toggle dropdown open/close
dropdownToggle.addEventListener("click", () => {
    dropdown.classList.toggle("open");
});

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target)) {
        dropdown.classList.remove("open");
    }
});

// Home button loads home content
homeButton.addEventListener("click", () => {
    loadHome();
});

// Submenu country/topic buttons
document.querySelectorAll(".dropdown-submenu .dropdown-item").forEach(item => {
    item.addEventListener("click", () => {
        const country = item.dataset.country;
        const topic = item.dataset.topic;
        dropdown.classList.remove("open");
        loadCountryTopic(country, topic);
    });
});

// Handle clicks on the country label itself (like "United States")
document.querySelectorAll(".country-header").forEach(button => {
    button.addEventListener("click", (e) => {
        e.stopPropagation(); // prevent submenu from immediately opening
        const country = button.dataset.country;
        dropdown.classList.remove("open");
        loadCountryOverview(country);
    });
});

// Initial load
loadHome();