async function loadPhotographers() {
    const search = document.getElementById("search")?.value || "";
    const ordering = document.getElementById("ordering")?.value || "-rating";
    const url = `/api/photographers/?search=${search}&ordering=${ordering}`;
    const response = await apiFetch(url);
    if (!response) return;
    const data = await response.json();
    const container = document.getElementById("photographers-list");
    container.innerHTML = "";

    (data.results || data).forEach(p => {
        container.innerHTML += `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5>${p.name}</h5>
                        <p>⭐ Рейтинг: ${p.rating}</p>
                        <p>💰 ${p.hourly_rate} руб./ч</p>
                        <p>⏱ Мин.: ${p.min_hours} ч.</p>
                    </div>
                </div>
            </div>`;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadPhotographers();
    document.getElementById("search")?.addEventListener("input", loadPhotographers);
    document.getElementById("ordering")?.addEventListener("change", loadPhotographers);
});