document.querySelectorAll("[data-url]").forEach((button) => {
  button.addEventListener("click", () => {
    const input = document.getElementById("url");
    input.value = button.dataset.url;
    input.focus();
  });
});

const form = document.getElementById("scan-form");
if (form) {
  form.addEventListener("submit", () => {
    const button = document.getElementById("scan-button");
    if (!button) return;
    button.disabled = true;
    button.querySelector("span").textContent = "Checking…";
  });
}
