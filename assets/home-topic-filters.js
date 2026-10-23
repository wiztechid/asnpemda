(() => {
  const grid = document.querySelector("[data-topic-filter-grid]");
  const controls = document.querySelector("[data-topic-filter-controls]");
  if (!grid || !controls) return;

  const buttons = [...controls.querySelectorAll("[data-topic-filter]")];
  const cards = [...grid.querySelectorAll(".article-card[data-topic]")];
  const status = document.querySelector("[data-topic-filter-status]");

  const applyFilter = (topic) => {
    let visible = 0;
    cards.forEach((card) => {
      const show = topic === "all" || card.dataset.topic === topic;
      card.hidden = !show;
      if (show) visible += 1;
    });
    buttons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.topicFilter === topic));
    });
    grid.classList.toggle("is-filtered", topic !== "all");
    if (status) status.textContent = `Menampilkan ${visible} artikel`;
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => applyFilter(button.dataset.topicFilter));
  });
  controls.hidden = false;
  applyFilter("all");
})();
