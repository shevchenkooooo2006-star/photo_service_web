async function loadLocations() {
    const response = await apiFetch("/api/locations/");
    if (!response) return;
    const data = await response.json();
    const container = document.getElementById("locations-list");
    container.innerHTML = "";

    (data.results || data).forEach(loc => {
        container.innerHTML += `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5>${loc.name}</h5>
                        <p>💰 ${loc.rent_price} руб./ч</p>
                    </div>
                </div>
            </div>`;
    });
}

document.addEventListener("DOMContentLoaded", loadLocations);