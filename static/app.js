// ---------- texts (English / German) ----------
// The backend only sends codes and numbers, all sentences live here.
const TEXT = {
    en: {
        tagline: "Find accommodation that fits your studies.",
        logout: "Logout",
        loginTitle: "Login or register",
        name: "Name (only for registering)",
        email: "Email",
        password: "Password (min. 6 characters)",
        login: "Login",
        register: "Register",
        profileTitle: "Your accommodation profile",
        university: "University",
        selectUniversity: "Select your university",
        arrival: "Expected arrival",
        end: "Accommodation needed until",
        rent: "Maximum monthly rent (€)",
        upfront: "Maximum upfront cost: rent + deposit (€)",
        commute: "Maximum commute (minutes)",
        room: "Room type",
        furnishedLabel: "Furnished",
        yes: "Yes",
        no: "No",
        private: "Private",
        shared: "Shared",
        find: "Find my matches",
        matchesTitle: "Best matches",
        savedTitle: "Saved accommodations",
        tasksTitle: "Arrival planner",
        furnishedWord: "furnished",
        unfurnished: "unfurnished",
        perMonth: "/ month",
        minutes: "minutes commute",
        freeFrom: "Available from",
        deposit: "Deposit",
        why: "Why it matches",
        save: "Save",
        savedBadge: "Saved ✓",
        remove: "Remove",
        interest: "Express interest",
        interestSent: "Interest sent ✓",
        matchOne: "suitable accommodation found",
        matchCount: "suitable accommodations found",
        noMatches: "No suitable accommodation found. Try a higher rent or commute limit.",
        noSaved: "Nothing saved yet.",
        tasksDone: "completed",
        // reasons (see matching.py)
        reason_furnished: "Furnished, as you requested",
        reason_room_private: "Matches your private room requirement",
        reason_room_shared: "Matches your shared room requirement",
        reason_rent: "€{saving} below your €{max} maximum rent",
        reason_commute: "{minutes}-minute commute within your {max}-minute limit",
        reason_dates: "Available for your required dates",
        // arrival tasks (keys from database.py)
        task_accommodation: "Accommodation confirmed",
        task_accommodation_text: "Confirm your accommodation and keep the booking details.",
        task_university: "University registration",
        task_university_text: "Complete the enrolment steps with your university.",
        task_registration: "Residence registration",
        task_registration_text: "Register your address with the local authority after arriving.",
        task_bank: "Bank account",
        task_bank_text: "Open a bank account if you need one.",
        task_insurance: "Health insurance",
        task_insurance_text: "Make sure your health insurance is arranged.",
        // messages
        loginFailed: "Wrong email or password.",
        registerFailed: "Registration failed. Please try again.",
        name_missing: "Please enter your name.",
        email_invalid: "Please enter a valid email address.",
        password_short: "The password needs at least 6 characters.",
        email_taken: "This email is already registered. Try logging in.",
        serverError: "Could not reach the server.",
        chooseUniversity: "Please select your university.",
        profileInvalid: "Please check your profile values.",
        loading: "Finding matches...",
        saveFailed: "Could not save this accommodation.",
        interestFailed: "Could not send your interest.",
        interestOk: "Your interest was sent.",
        taskFailed: "Could not update this task."
    },
    de: {
        tagline: "Finde eine Unterkunft, die zu deinem Studium passt.",
        logout: "Abmelden",
        loginTitle: "Anmelden oder registrieren",
        name: "Name (nur zum Registrieren)",
        email: "E-Mail",
        password: "Passwort (mind. 6 Zeichen)",
        login: "Anmelden",
        register: "Registrieren",
        profileTitle: "Dein Unterkunftsprofil",
        university: "Universität / Hochschule",
        selectUniversity: "Hochschule auswählen",
        arrival: "Voraussichtliche Ankunft",
        end: "Unterkunft benötigt bis",
        rent: "Maximale Monatsmiete (€)",
        upfront: "Maximale Anfangskosten: Miete + Kaution (€)",
        commute: "Maximale Pendelzeit (Minuten)",
        room: "Zimmertyp",
        furnishedLabel: "Möbliert",
        yes: "Ja",
        no: "Nein",
        private: "Privat",
        shared: "Geteilt",
        find: "Passende Unterkünfte finden",
        matchesTitle: "Beste Treffer",
        savedTitle: "Gespeicherte Unterkünfte",
        tasksTitle: "Ankunftsplaner",
        furnishedWord: "möbliert",
        unfurnished: "unmöbliert",
        perMonth: "/ Monat",
        minutes: "Minuten Pendelzeit",
        freeFrom: "Verfügbar ab",
        deposit: "Kaution",
        why: "Warum es passt",
        save: "Speichern",
        savedBadge: "Gespeichert ✓",
        remove: "Entfernen",
        interest: "Interesse bekunden",
        interestSent: "Interesse gesendet ✓",
        matchOne: "passende Unterkunft gefunden",
        matchCount: "passende Unterkünfte gefunden",
        noMatches: "Keine passende Unterkunft gefunden. Erhöhe Miete oder Pendelzeit.",
        noSaved: "Noch nichts gespeichert.",
        tasksDone: "erledigt",
        reason_furnished: "Möbliert, wie gewünscht",
        reason_room_private: "Entspricht deinem Wunsch nach einem privaten Zimmer",
        reason_room_shared: "Entspricht deinem Wunsch nach einem geteilten Zimmer",
        reason_rent: "€{saving} unter deiner maximalen Miete von €{max}",
        reason_commute: "{minutes} Minuten Pendelzeit, innerhalb deines Limits von {max} Minuten",
        reason_dates: "Für deinen gewünschten Zeitraum verfügbar",
        task_accommodation: "Unterkunft bestätigt",
        task_accommodation_text: "Bestätige deine Unterkunft und bewahre die Buchungsdaten auf.",
        task_university: "Immatrikulation",
        task_university_text: "Erledige die Einschreibung an deiner Hochschule.",
        task_registration: "Anmeldung des Wohnsitzes",
        task_registration_text: "Melde deine Adresse nach der Ankunft bei der Behörde an.",
        task_bank: "Bankkonto",
        task_bank_text: "Eröffne ein Bankkonto, falls du eines brauchst.",
        task_insurance: "Krankenversicherung",
        task_insurance_text: "Stelle sicher, dass deine Krankenversicherung geregelt ist.",
        loginFailed: "E-Mail oder Passwort falsch.",
        registerFailed: "Registrierung fehlgeschlagen. Bitte versuche es erneut.",
        name_missing: "Bitte gib deinen Namen ein.",
        email_invalid: "Bitte gib eine gültige E-Mail-Adresse ein.",
        password_short: "Das Passwort braucht mindestens 6 Zeichen.",
        email_taken: "Diese E-Mail ist bereits registriert. Versuche dich anzumelden.",
        serverError: "Server nicht erreichbar.",
        chooseUniversity: "Bitte wähle deine Hochschule.",
        profileInvalid: "Bitte prüfe die Werte in deinem Profil.",
        loading: "Suche läuft...",
        saveFailed: "Unterkunft konnte nicht gespeichert werden.",
        interestFailed: "Interesse konnte nicht gesendet werden.",
        interestOk: "Dein Interesse wurde gesendet.",
        taskFailed: "Aufgabe konnte nicht aktualisiert werden."
    }
};

// ---------- state ----------
let language = "en";
let universities = [];
let matches = [];
let savedRooms = [];
let interestIds = [];
let tasks = [];

try {
    language = localStorage.getItem("language") || "en";
} catch (e) {
    // no localStorage available, stay with English
}

const $ = id => document.getElementById(id);

function t(key) {
    return TEXT[language][key] || key;
}

function esc(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// ---------- helpers ----------

// Small wrapper around fetch. Returns {ok, data}.
async function api(path, method = "GET", body = null) {
    const options = { method: method, headers: { "Content-Type": "application/json" } };
    if (body) {
        options.body = JSON.stringify(body);
    }
    try {
        const response = await fetch("/api" + path, options);
        const data = await response.json();
        return { ok: response.ok, data: data };
    } catch (e) {
        return { ok: false, data: null, networkError: true };
    }
}

// Shows a message by its text key, so it can change when the language changes.
function say(id, key, kind = "") {
    const element = $(id);
    element.dataset.key = key;
    element.className = "message " + kind;
    element.textContent = key ? t(key) : "";
}

function roomName(room) {
    return t(room.room_type === "PRIVATE" ? "private" : "shared") + ", " +
        t(room.furnished ? "furnishedWord" : "unfurnished") + " – " + esc(room.city);
}

function reasonText(reason) {
    let text = t("reason_" + reason.code);
    for (const name in reason) {
        text = text.replace("{" + name + "}", reason[name]);
    }
    return text;
}

// ---------- language ----------

function applyTexts() {
    document.querySelectorAll("[data-i18n]").forEach(element => {
        element.textContent = t(element.dataset.i18n);
    });
    document.querySelectorAll(".message").forEach(element => {
        if (element.dataset.key) {
            element.textContent = t(element.dataset.key);
        }
    });
}

function setLanguage(lang) {
    language = lang;
    try {
        localStorage.setItem("language", lang);
    } catch (e) {
        // ignore
    }
    document.documentElement.lang = lang;
    $("enButton").classList.toggle("active", lang === "en");
    $("deButton").classList.toggle("active", lang === "de");
    applyTexts();
    showMatches();
    showSaved();
    showTasks();
}

// ---------- login ----------

async function submitAuth(mode) {
    const body = { email: $("email").value, password: $("password").value };
    if (mode === "register") {
        body.name = $("name").value;
    }

    const result = await api("/" + mode, "POST", body);
    if (result.networkError) {
        say("authMessage", "serverError", "bad");
    } else if (!result.ok) {
        // the backend sends a code like "password_short" for register errors
        const known = result.data && TEXT[language][result.data.error];
        say("authMessage", mode === "login" ? "loginFailed" : (known ? result.data.error : "registerFailed"), "bad");
    } else {
        say("authMessage", "");
        $("password").value = "";
        await startApp();
    }
}

async function logout() {
    await api("/logout", "POST");
    matches = [];
    savedRooms = [];
    tasks = [];
    $("authBox").hidden = false;
    $("appBox").hidden = true;
    $("logoutButton").hidden = true;
    showMatches();
}

// Called after login and also on page load (the session cookie may still be valid).
async function startApp() {
    const me = await api("/me");
    if (!me.ok) {
        return;
    }
    $("authBox").hidden = true;
    $("appBox").hidden = false;
    $("logoutButton").hidden = false;

    const profile = await api("/profile");
    if (profile.data) {
        fillProfileForm(profile.data);
        await loadMatches();
    }
    await loadSaved();
    await loadInterests();
    await loadTasks();
}

// ---------- profile and matches ----------

async function loadUniversities() {
    const result = await api("/universities");
    universities = result.data || [];

    const select = $("university");
    select.innerHTML = '<option value="" data-i18n="selectUniversity"></option>';
    universities.forEach(u => {
        const option = document.createElement("option");
        option.value = u.id;
        option.textContent = u.name + " — " + u.city;
        select.appendChild(option);
    });
    applyTexts();
}

function fillProfileForm(p) {
    $("university").value = p.university_id;
    $("arrival").value = p.arrival_date;
    $("end").value = p.end_date;
    $("rent").value = p.max_rent;
    $("upfront").value = p.max_upfront;
    $("commute").value = p.max_commute;
    $("room").value = p.room_type;
    $("furnished").value = p.furnished;
}

async function findMatches() {
    if (!$("university").value) {
        say("profileMessage", "chooseUniversity", "bad");
        return;
    }

    say("profileMessage", "loading");
    const result = await api("/profile", "POST", {
        university_id: $("university").value,
        arrival_date: $("arrival").value,
        end_date: $("end").value,
        max_rent: $("rent").value,
        max_upfront: $("upfront").value,
        max_commute: $("commute").value,
        room_type: $("room").value,
        furnished: $("furnished").value === "1"
    });

    if (!result.ok) {
        say("profileMessage", result.networkError ? "serverError" : "profileInvalid", "bad");
        return;
    }
    say("profileMessage", "");
    await loadMatches();
}

async function loadMatches() {
    const result = await api("/matches");
    matches = result.ok ? result.data : [];
    showMatches();
}

function showMatches() {
    $("matchCount").textContent = matches.length + " " + t(matches.length === 1 ? "matchOne" : "matchCount");

    if (matches.length === 0) {
        $("matches").innerHTML = '<p class="empty">' + t("noMatches") + "</p>";
        return;
    }

    $("matches").innerHTML = matches.map(room => {
        const reasons = room.match_reasons.map(r => "<li>✓ " + reasonText(r) + "</li>").join("");
        const isSaved = savedRooms.some(s => s.id === room.id);
        const interestSent = interestIds.includes(room.id);

        return `
        <article class="card">
            <div class="card-top">
                <h3>${roomName(room)}</h3>
                <span class="score">${room.match_score}%</span>
            </div>
            <div class="price">€${room.monthly_rent} ${t("perMonth")}</div>
            <div class="details">
                ${t("deposit")}: €${room.deposit}<br>
                🚆 ${room.commute_minutes} ${t("minutes")}<br>
                📅 ${t("freeFrom")} ${room.available_from}
            </div>
            <div class="reasons">
                <b>${t("why")}</b>
                <ul>${reasons}</ul>
            </div>
            <div class="row">
                <button ${isSaved ? "disabled" : ""} onclick="saveRoom(${room.id})">
                    ${isSaved ? t("savedBadge") : t("save")}
                </button>
                <button class="secondary" ${interestSent ? "disabled" : ""} onclick="sendInterest(${room.id})">
                    ${interestSent ? t("interestSent") : t("interest")}
                </button>
            </div>
        </article>`;
    }).join("");
}

// ---------- saved accommodations ----------

async function loadSaved() {
    const result = await api("/saved");
    savedRooms = result.ok ? result.data : [];
    showSaved();
    showMatches();
}

function showSaved() {
    if (savedRooms.length === 0) {
        $("saved").innerHTML = '<p class="empty">' + t("noSaved") + "</p>";
        return;
    }

    $("saved").innerHTML = savedRooms.map(room => {
        const interestSent = interestIds.includes(room.id);
        return `
        <article class="card">
            <h3>${roomName(room)}</h3>
            <div class="price">€${room.monthly_rent} ${t("perMonth")}</div>
            <div class="details">${t("freeFrom")} ${room.available_from}</div>
            <div class="row">
                <button class="danger" onclick="removeSaved(${room.id})">${t("remove")}</button>
                <button class="secondary" ${interestSent ? "disabled" : ""} onclick="sendInterest(${room.id})">
                    ${interestSent ? t("interestSent") : t("interest")}
                </button>
            </div>
        </article>`;
    }).join("");
}

async function saveRoom(id) {
    const result = await api("/saved/" + id, "POST");
    if (!result.ok) {
        say("matchMessage", "saveFailed", "bad");
        return;
    }
    say("matchMessage", "");
    await loadSaved();
}

async function removeSaved(id) {
    await api("/saved/" + id, "DELETE");
    await loadSaved();
}

// ---------- expression of interest ----------

async function loadInterests() {
    const result = await api("/interest");
    interestIds = result.ok ? result.data : [];
    showMatches();
    showSaved();
}

async function sendInterest(id) {
    const result = await api("/interest/" + id, "POST");
    if (!result.ok) {
        say("matchMessage", "interestFailed", "bad");
        return;
    }
    say("matchMessage", "interestOk", "ok");
    await loadInterests();
}

// ---------- arrival planner ----------

async function loadTasks() {
    const result = await api("/tasks");
    tasks = result.ok ? result.data : [];
    showTasks();
}

function showTasks() {
    const done = tasks.filter(task => task.done).length;
    $("taskProgress").textContent = tasks.length ? done + "/" + tasks.length + " " + t("tasksDone") : "";

    $("tasks").innerHTML = tasks.map(task => `
        <label class="task ${task.done ? "done" : ""}">
            <input type="checkbox" ${task.done ? "checked" : ""} onchange="toggleTask(${task.id}, this.checked)">
            <span><b>${t("task_" + task.task_key)}</b><br>
            <small>${t("task_" + task.task_key + "_text")}</small></span>
        </label>`).join("");
}

async function toggleTask(id, done) {
    const result = await api("/tasks/" + id, "PATCH", { done: done });
    if (!result.ok) {
        say("taskMessage", "taskFailed", "bad");
        await loadTasks();  // put the checkbox back to the saved state
        return;
    }
    say("taskMessage", "");
    await loadTasks();
}

// ---------- start ----------

window.addEventListener("DOMContentLoaded", async () => {
    await loadUniversities();
    setLanguage(language);
    await startApp();  // does nothing if the user is not logged in
});
