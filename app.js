// Configure your backend base URL here
const BASE_URL = localStorage.getItem("askutd_base_url") || "http://localhost:8000";

const e = React.createElement;

function App() {
  const [query, setQuery] = React.useState("");
  const [answer, setAnswer] = React.useState("");
  const [sources, setSources] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  async function ask() {
    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);
    try {
      const res = await fetch(`${BASE_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        throw new Error(j.detail || `HTTP ${res.status}`);
      }
      const j = await res.json();
      setAnswer(j.answer || "");
      setSources(j.sources || []);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  return e("div", { className: "container" },
    e("h1", null, "AskUTD – UTD Resources Assistant (MVP)"),
    e("p", { className: "caption" }, "Backend: ", BASE_URL, "  ",
      e("button", {
        onClick: () => {
          const url = prompt("Enter backend URL", BASE_URL);
          if (url) {
            localStorage.setItem("askutd_base_url", url);
            location.reload();
          }
        }
      }, "change")),
    e("div", { className: "row" },
      e("input", {
        value: query,
        onChange: (ev) => setQuery(ev.target.value),
        placeholder: "e.g., What is CPT and how do I apply?",
      }),
      e("button", { onClick: ask, disabled: loading || !query.trim() }, loading ? "Asking..." : "Ask")
    ),
    error && e("div", { className: "error" }, error),
    answer && e("div", { className: "card" },
      e("h3", null, "Answer"),
      e("p", null, answer),
      sources.length ? e("p", { className: "sources" }, "Sources: ", sources.join(", ")) : null
    ),
    e("details", null,
      e("summary", null, "How to run"),
      e("pre", null, `1) Start backend on port 8000
2) Open this file or serve: python -m http.server 5173
3) Ask a question`)
    )
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(e(App));
