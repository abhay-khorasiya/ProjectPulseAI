import {
  useEffect,
  useState,
} from "react";

import StatusActionButton
  from "../components/StatusActionButton";

import {
  getProjectMemory,
  searchProjectMemory,
} from "../services/api";


function MemoryPage() {
  const [items, setItems] =
    useState([]);

  const [query, setQuery] =
    useState("");

  const [filter, setFilter] =
    useState("all");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  async function loadMemory() {
    setLoading(true);
    setError("");

    try {
      let data;

      if (query.trim()) {
        data =
          await searchProjectMemory(
            query.trim()
          );
      } else {
        data =
          await getProjectMemory();
      }

      setItems(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadMemory();
  }, []);


  async function handleSearch(event) {
    event.preventDefault();

    await loadMemory();
  }


  const visibleItems =
    filter === "all"
      ? items
      : items.filter(
          (item) =>
            item.item_type === filter
        );


  return (
    <div className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">
            SEARCHABLE PROJECT MEMORY
          </span>

          <h1>
            Project Memory
          </h1>

          <p>
            Find previous actions,
            decisions, deadlines and
            approvals without searching
            through endless chats.
          </p>
        </div>
      </header>


      <div className="panel memory-search-panel">
        <form
          className="search-form"
          onSubmit={handleSearch}
        >
          <input
            type="text"
            className="search-input"
            placeholder="Search marble, Abhay, Friday, approval..."
            value={query}
            onChange={(event) =>
              setQuery(
                event.target.value
              )
            }
          />

          <button
            type="submit"
            className="primary-button"
          >
            Search Memory
          </button>
        </form>


        <div className="filter-row">
          {[
            ["all", "All"],
            ["task", "Tasks"],
            [
              "decision",
              "Decisions",
            ],
            [
              "approval",
              "Approvals",
            ],
          ].map(
            ([value, label]) => (
              <button
                type="button"
                key={value}
                className={
                  filter === value
                    ? "filter-button active"
                    : "filter-button"
                }
                onClick={() =>
                  setFilter(value)
                }
              >
                {label}
              </button>
            )
          )}
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <div className="memory-results-header">
        <h2>
          Project Intelligence
        </h2>

        <span>
          {visibleItems.length}
          {" "}
          results
        </span>
      </div>


      {loading ? (
        <div className="panel empty-state">
          Loading project memory...
        </div>
      ) : visibleItems.length === 0 ? (
        <div className="panel empty-state">
          <h3>
            No results found
          </h3>

          <p>
            Try another search term or
            analyze another conversation.
          </p>
        </div>
      ) : (
        <div className="memory-page-list">
          {visibleItems.map(
            (item) => (
              <div
                className="memory-card"
                key={item.id}
              >
                <div
                  className={
                    `memory-card-icon ${item.item_type}`
                  }
                >
                  {item.item_type
                    .charAt(0)
                    .toUpperCase()}
                </div>


                <div className="memory-card-content">
                  <div className="memory-card-top">
                    <span
                      className={
                        `type-badge ${item.item_type}`
                      }
                    >
                      {item.item_type}
                    </span>

                    <span className="source-text">
                      {item.source}
                    </span>
                  </div>


                  <h3>
                    {item.content}
                  </h3>


                  <div className="memory-detail-row">
                    {item.responsible && (
                      <span>
                        Responsible:
                        {" "}
                        <strong>
                          {item.responsible}
                        </strong>
                      </span>
                    )}

                    {item.deadline && (
                      <span>
                        Deadline:
                        {" "}
                        <strong>
                          {item.deadline}
                        </strong>
                      </span>
                    )}

                    <span>
                      Status:
                      {" "}
                      <strong>
                        {item.status}
                      </strong>
                    </span>

                    <span>
                      Conversation #
                      {item.conversation_id}
                    </span>
                  </div>


                  <StatusActionButton
                    item={item}
                    onUpdated={loadMemory}
                  />
                </div>
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}


export default MemoryPage;