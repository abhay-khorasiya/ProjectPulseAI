const menuItems = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: "⌂",
  },
  {
    id: "analyze",
    label: "Analyze Conversation",
    icon: "✦",
  },
  {
    id: "memory",
    label: "Project Memory",
    icon: "⌕",
  },
];

function Sidebar({
  activePage,
  onPageChange,
}) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          P
        </div>

        <div>
          <h2>ProjectPulse</h2>
          <span>AI Communication Layer</span>
        </div>
      </div>

      <div className="nav-title">
        WORKSPACE
      </div>

      <nav className="navigation">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={
              activePage === item.id
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() =>
              onPageChange(item.id)
            }
          >
            <span className="nav-icon">
              {item.icon}
            </span>

            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-info">
        <p>ArchScale Guild</p>

        <span>
          Hackathon Challenge AS-02
        </span>

        <div className="status-dot-row">
          <span className="online-dot" />
          Local intelligence active
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;