/* Базовая работа с API */
const API_BASE = "/api";

function getToken() {
    return localStorage.getItem("access_token");
}

async function apiFetch(url, options = {}) {
    const token = getToken();
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    const response = await fetch(url, { ...options, headers });
    if (response.status === 401) {
        localStorage.removeItem("access_token");
        window.location.href = "/login/";
        return null;
    }
    return response;
}