NProgress.start();

const tooltipTriggerList = document.querySelectorAll(
  '[data-bs-toggle="tooltip"]'
);
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

function message(username) {
  localStorage.setItem("message", username);
  window.location.href = "/chat";
}

function toggleTheme() {
  const theme = document.body.getAttribute("data-bs-theme");
  const _theme = theme === "dark" ? "light" : "dark";
  document.body.setAttribute("data-bs-theme", _theme);
  localStorage.setItem("theme", _theme);
}

document.addEventListener("DOMContentLoaded", () => {
  const theme = document.body.getAttribute("data-bs-theme");
  const _theme = localStorage.getItem("theme");
  if (theme !== _theme) toggleTheme();

  let props = localStorage.getItem("props") || "{}";
  props = JSON.parse(props);

  if (props?.chat) {
    const chatElement = document.getElementById("chat-count");
    if (chatElement) chatElement.innerText = props?.chat;
    document.getElementById("chat-badge").classList.remove("d-none");
  }

  if (props?.notification) {
    const notificationElement = document.getElementById("notification-count");
    if (notificationElement)
      notificationElement.innerText = props?.notification;
    document.getElementById("notification-badge").classList.remove("d-none");
  }

  if (props?.ad_count) {
    const adElement = document.getElementById("ad-count");
    if (adElement) adElement.innerText = props?.ad_count;
  }

  if (props?.image) {
    const profileElement = document.getElementById("profile-picture");
    if (profileElement) profileElement.setAttribute("src", props?.image);
  }

  const searchField = document.querySelector(".search-field");
  const hideElements = document.querySelectorAll(".hide-on-search");

  if (searchField && hideElements.length > 0) {
    searchField.addEventListener("focus", () => {
      hideElements.forEach((element) => {
        element.style.display = "none";
      });
      searchField.style.width = "20rem";
    });

    searchField.addEventListener("blur", () => {
      hideElements.forEach((element) => {
        element.style.display = null;
      });
      searchField.style.width = "10rem";
    });

    if (searchField.value.length > 0) {
      hideElements.forEach((element) => {
        element.style.display = "none";
      });
      searchField.style.width = "20rem";
    }
  }

  NProgress.done();
});
