async function loadBookings() {
    const response = await apiFetch("/api/bookings/");
    if (!response) return;
    const data = await response.json();
    const container = document.getElementById("bookings-list");
    container.innerHTML = "";

    (data.results || data).forEach(b => {
        const state = b.is_cancelled ? "❌ ОТМЕНЕНО" : "✅ активно";
        const cancelBtn = b.is_cancelled ? "" :
            `<button class="btn btn-sm btn-danger" onclick="cancelBooking(${b.id})">Отменить</button>`;
        container.innerHTML += `
            <div class="card mb-2">
                <div class="card-body">
                    <strong>#${b.id}</strong> ${b.client_detail.name} → ${b.photographer_detail.name}
                    в ${b.location_detail.name} на ${b.shoot_date}
                    (${b.hours} ч.) <b>${state}</b>
                    <br>Итого: <b>${b.total_cost} руб.</b>
                    ${cancelBtn}
                </div>
            </div>`;
    });
}

async function cancelBooking(id) {
    if (!confirm("Отменить бронирование?")) return;
    const response = await apiFetch(`/api/bookings/${id}/cancel/`, { method: "POST" });
    if (response && response.ok) {
        loadBookings();
    } else {
        alert("Не удалось отменить.");
    }
}

// При открытии модалки загружаем фотографов, локации, клиентов
async function fillSelects() {
    const [ph, loc] = await Promise.all([
        apiFetch("/api/photographers/").then(r => r.json()),
        apiFetch("/api/locations/").then(r => r.json()),
    ]);
    const phSelect = document.getElementById("photographer");
    const locSelect = document.getElementById("location");
    (ph.results || ph).forEach(p => {
        phSelect.innerHTML += `<option value="${p.id}">${p.name}</option>`;
    });
    (loc.results || loc).forEach(l => {
        locSelect.innerHTML += `<option value="${l.id}">${l.name}</option>`;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadBookings();
    document.querySelector("#createModal").addEventListener("show.bs.modal", fillSelects);

    document.getElementById("booking-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            photographer: parseInt(document.getElementById("photographer").value),
            location: parseInt(document.getElementById("location").value),
            client: parseInt(document.getElementById("client").value),
            shoot_date: document.getElementById("shoot_date").value,
            hours: parseInt(document.getElementById("hours").value),
            need_makeup: document.getElementById("need_makeup").checked,
        };
        const response = await apiFetch("/api/bookings/", {
            method: "POST",
            body: JSON.stringify(payload),
        });
        const errorEl = document.getElementById("form-error");
        errorEl.textContent = "";
        if (response && response.ok) {
            document.getElementById("createModal").querySelector(".btn-close").click();
            loadBookings();
        } else {
            const err = await response.json();
            errorEl.textContent = JSON.stringify(err);
        }
    });
});