(() => {
  const root = document.querySelector(".reader-engagement[data-article]");
  if (!root) return;
  const article = root.dataset.article;
  const commentList = root.querySelector("[data-comment-list]");
  const commentForm = root.querySelector("[data-comment-form]");
  const commentStatus = root.querySelector("[data-comment-status]");
  const feedbackStatus = root.querySelector("[data-feedback-status]");
  const feedbackButtons = [...root.querySelectorAll("[data-vote]")];

  const setStatus = (node, message) => { if (node) node.textContent = message || ""; };

  function renderComments(comments) {
    commentList.replaceChildren();
    if (!comments.length) {
      const empty = document.createElement("p");
      empty.textContent = "Belum ada komentar yang ditampilkan. Jadilah yang pertama berbagi tanggapan.";
      commentList.append(empty);
      return;
    }
    for (const item of comments) {
      const card = document.createElement("article");
      card.className = "comment-item";
      const header = document.createElement("div");
      const name = document.createElement("strong");
      name.textContent = item.name;
      const time = document.createElement("time");
      const date = new Date(item.createdAt);
      time.dateTime = date.toISOString();
      time.textContent = new Intl.DateTimeFormat("id-ID", { dateStyle: "medium" }).format(date);
      const text = document.createElement("p");
      text.textContent = item.comment;
      header.append(name, time);
      card.append(header, text);
      commentList.append(card);
    }
  }

  async function load() {
    try {
      const [commentsResponse, feedbackResponse] = await Promise.all([
        fetch(`/api/comments?article=${encodeURIComponent(article)}`, { cache: "no-store" }),
        fetch(`/api/feedback?article=${encodeURIComponent(article)}`, { cache: "no-store" }),
      ]);
      if (!commentsResponse.ok || !feedbackResponse.ok) throw new Error("Layanan belum tersedia.");
      const comments = await commentsResponse.json();
      const counts = await feedbackResponse.json();
      renderComments(comments.comments || []);
      for (const vote of ["yes", "no"]) {
        const target = root.querySelector(`[data-count="${vote}"]`);
        if (target) target.textContent = String(counts[vote] || 0);
      }
    } catch {
      commentList.textContent = "Komentar belum dapat dimuat. Silakan coba lagi nanti.";
    }
  }

  for (const button of feedbackButtons) {
    button.addEventListener("click", async () => {
      button.disabled = true;
      setStatus(feedbackStatus, "Menyimpan umpan balik…");
      try {
        const response = await fetch(`/api/feedback?article=${encodeURIComponent(article)}`, {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ vote: button.dataset.vote }),
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || "Belum berhasil menyimpan.");
        for (const vote of ["yes", "no"]) {
          const target = root.querySelector(`[data-count="${vote}"]`);
          if (target) target.textContent = String(result.counts[vote] || 0);
        }
        setStatus(feedbackStatus, "Terima kasih, masukan Anda tercatat.");
      } catch (error) {
        setStatus(feedbackStatus, error.message || "Umpan balik belum dapat disimpan.");
        button.disabled = false;
      }
    });
  }

  commentForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    setStatus(commentStatus, "");
    const data = new FormData(commentForm);
    const token = data.get("cf-turnstile-response");
    const button = commentForm.querySelector(".comment-submit");
    button.disabled = true;
    try {
      const response = await fetch(`/api/comments?article=${encodeURIComponent(article)}`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: data.get("name"), comment: data.get("comment"), website: data.get("website"), turnstile: token }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Komentar belum dapat dikirim.");
      commentForm.reset();
      if (window.turnstile) window.turnstile.reset();
      setStatus(commentStatus, result.message || "Komentar diterima dan menunggu tinjauan sebelum ditampilkan.");
    } catch (error) {
      setStatus(commentStatus, error.message || "Komentar belum dapat dikirim. Silakan coba lagi.");
      if (window.turnstile) window.turnstile.reset();
    } finally {
      button.disabled = false;
    }
  });

  load();
})();
