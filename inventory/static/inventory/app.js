document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("recipe-search-form");
  const results = document.getElementById("recipe-results");
  const endpoint = form?.dataset?.endpoint;

  if (!form || !results || !endpoint) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = form.querySelector('input[name="q"]').value;

    try {
      const res = await fetch(endpoint + "?q=" + encodeURIComponent(q));
      const html = await res.text();
      results.innerHTML = html;
    } catch (err) {
      results.innerHTML = "<p>検索に失敗しました。通信状況を確認してもう一度お試しください。</p>";
    }
  });
});