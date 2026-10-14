"use strict";

const card = document.getElementById("session-card");
const statusMessage = document.getElementById("status");
const errorMessage = document.getElementById("error");
const loginView = document.getElementById("login-view");
const userView = document.getElementById("user-view");
const loginForm = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const loginButton = document.getElementById("login-button");
const logoutButton = document.getElementById("logout-button");
const welcomeTitle = document.getElementById("welcome-title");
const userEmail = document.getElementById("user-email");
let busy = false;

function setBusy(value, message = "") {
  busy = value;
  card.setAttribute("aria-busy", String(value));
  emailInput.disabled = value;
  passwordInput.disabled = value;
  loginButton.disabled = value;
  logoutButton.disabled = value;
  statusMessage.textContent = message;
}

function clearError() {
  errorMessage.textContent = "";
  errorMessage.hidden = true;
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}

function showLogin() {
  loginView.hidden = false;
  userView.hidden = true;
  welcomeTitle.textContent = "Bienvenido";
  userEmail.textContent = "";
}

function showUser(user) {
  welcomeTitle.textContent = `Bienvenido, ${user.name}`;
  userEmail.textContent = user.email;
  loginView.hidden = true;
  userView.hidden = false;
}

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(path, { ...options, credentials: "same-origin" });
  } catch {
    throw new Error("No se pudo conectar con el servidor. Inténtalo de nuevo.");
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("El servidor devolvió una respuesta inesperada. Inténtalo de nuevo.");
  }

  if (!response.ok) {
    const message = typeof data?.error === "string"
      ? data.error
      : "No se pudo completar la solicitud. Inténtalo de nuevo.";
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }
  return data;
}

function sessionUser(data) {
  const user = data?.user;
  if (!user || typeof user.name !== "string" || typeof user.email !== "string") {
    throw new Error("El servidor devolvió una sesión inesperada. Inténtalo de nuevo.");
  }
  return user;
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) return;
  clearError();
  const credentials = { email: emailInput.value.trim(), password: passwordInput.value };
  setBusy(true, "Iniciando sesión…");
  let authenticated = false;
  try {
    const data = await request("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });
    showUser(sessionUser(data));
    authenticated = true;
  } catch (error) {
    showError(error.message);
  } finally {
    passwordInput.value = "";
    setBusy(false);
    if (authenticated) welcomeTitle.focus();
    else passwordInput.focus();
  }
});

logoutButton.addEventListener("click", async () => {
  if (busy) return;
  clearError();
  setBusy(true, "Cerrando sesión…");
  let loggedOut = false;
  try {
    const data = await request("/api/logout", { method: "POST" });
    if (data?.ok !== true) {
      throw new Error("El servidor devolvió una respuesta inesperada. Inténtalo de nuevo.");
    }
    passwordInput.value = "";
    showLogin();
    loggedOut = true;
  } catch (error) {
    showError(error.message);
  } finally {
    setBusy(false, loggedOut ? "Sesión cerrada." : "");
    if (loggedOut) emailInput.focus();
  }
});

async function checkSession() {
  setBusy(true, "Comprobando tu sesión…");
  try {
    showUser(sessionUser(await request("/api/me")));
  } catch (error) {
    showLogin();
    if (error.status !== 401) showError(error.message);
  } finally {
    setBusy(false);
  }
}

checkSession();
