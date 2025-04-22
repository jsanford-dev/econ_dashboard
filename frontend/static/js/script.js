document.addEventListener("DOMContentLoaded", () => {
    const dashboard = document.getElementById("dashboard");
    const homeButton = document.getElementById("home-button");
    const dropdownToggle = document.querySelector(".dropdown-toggle");
    const dropdown = document.querySelector(".dropdown");

    if (!dashboard) return; // Don't run if dashboard doesn't exist

    // Render homepage content
    function loadHome() {
        dashboard.innerHTML = `
            <div class='data-card'>
                <h2>Welcome to the Macro Dashboard</h2>
                <p>Select a country to view macroeconomic data</p>
            </div>
        `;
    }

    // Render overview data for a country
    function loadCountryOverview(country) {
        const countryLabel = country.replace("-", " ").toUpperCase();

        dashboard.innerHTML = `
            <div class='data-card'>
                <h2>${countryLabel} Overview</h2>
                <p>Loading summary data...</p>
            </div>
        `;

        fetch(`/api/data/${country}/overview`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                dashboard.innerHTML = renderTopicData(countryLabel, "Overview", data);
            })
            .catch(error => {
                dashboard.innerHTML = `
                    <div class='data-card'>
                        <h2>${countryLabel} Overview</h2>
                        <p class="error">Failed to load overview: ${error.message}</p>
                    </div>
                `;
            });
    }

    // Render data for a specific topic
    function loadCountryTopic(country, topic) {
        const countryLabel = country.replace("-", " ").toUpperCase();
        const topicLabel = topic.charAt(0).toUpperCase() + topic.slice(1);

        dashboard.innerHTML = `
            <div class='data-card'>
                <h2>${countryLabel} - ${topicLabel}</h2>
                <p>Loading data for ${topicLabel}...</p>
            </div>
        `;

        fetch(`/api/data/${country}/${topic}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                dashboard.innerHTML = renderTopicData(countryLabel, topicLabel, data);
            })
            .catch(error => {
                dashboard.innerHTML = `
                    <div class='data-card'>
                        <h2>${countryLabel} - ${topicLabel}</h2>
                        <p class="error">Failed to load data: ${error.message}</p>
                    </div>
                `;
            });
    }

    // Format the data as a card
    function renderTopicData(country, topic, data) {
        return `
            <div class='data-card'>
                <h2>${country} - ${topic}</h2>
                <pre>${JSON.stringify(data, null, 2)}</pre>
            </div>
        `;
    }

    // Toggle dropdown open/close
    if (dropdownToggle && dropdown) {
        dropdownToggle.addEventListener("click", () => {
            dropdown.classList.toggle("open");
        });

        document.addEventListener("click", (e) => {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove("open");
            }
        });
    }

    // Home button
    if (homeButton) {
        homeButton.addEventListener("click", () => {
            loadHome();
        });
    }

    // Submenu topic buttons (e.g. Labour, Inflation)
    document.querySelectorAll(".dropdown-submenu .dropdown-item").forEach(item => {
        item.addEventListener("click", () => {
            const country = item.dataset.country;
            const topic = item.dataset.topic;
            dropdown.classList.remove("open");
            loadCountryTopic(country, topic);
        });
    });

    // Country overview links (e.g. clicking "United States")
    document.querySelectorAll(".country-header").forEach(button => {
        button.addEventListener("click", (e) => {
            e.stopPropagation();
            const country = button.dataset.country;
            dropdown.classList.remove("open");
            loadCountryOverview(country);
        });
    });

    // Initial page load behavior — only for root path
    if (window.location.pathname === "/") {
        loadHome();
    }
});
