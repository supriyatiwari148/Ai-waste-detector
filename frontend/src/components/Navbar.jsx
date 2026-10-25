const LINKS = [
  ["home", "Analyze"],
  ["guide", "Guide"],
  ["history", "History"],
];

export default function Navbar({ page, onNavigate }) {
  return (
    <header className="navbar">
      <div className="container nav-inner">
        <button className="brand" onClick={() => onNavigate("home")}>
          ♻️ <span>EcoSort AI</span>
        </button>
        <nav aria-label="Main">
          {LINKS.map(([id, label]) => (
            <button
              key={id}
              className={page === id ? "nav-link active" : "nav-link"}
              onClick={() => onNavigate(id)}
            >
              {label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}
