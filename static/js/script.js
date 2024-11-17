NProgress.start();

const tooltipTriggerList = document.querySelectorAll(
  '[data-bs-toggle="tooltip"]'
);
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

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

  NProgress.done();
});
