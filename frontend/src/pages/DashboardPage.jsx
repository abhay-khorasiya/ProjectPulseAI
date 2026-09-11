import {
  useCallback,
  useEffect,
  useState,
} from "react";

import StatusActionButton
  from "../components/StatusActionButton";

import {
  getDashboardStats,
  getProjectMemory,
} from "../services/api";


function DashboardPage({
  onAnalyzeClick,
}) {
  const [stats, setStats] =
    useState({
      conversations: 0,
      total_memory_items: 0,
      tasks: 0,
      open_tasks: 0,
      decisions: 0,
      pending_approvals: 0,
    });

  const [memory, setMemory] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  const loadDashboard =
    useCallback(
      async () => {
        setLoading(true);
        setError("");

        try {
          const [
            statsData,
            memoryData,
          ] = await Promise.all([
            getDashboardStats(),
            getProjectMemory(),
          ]);

          setStats(statsData);
          setMemory(memoryData);
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      },
      []
    );


  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);


  const recentItems =
    memory.slice(
      0,
      6
    );


  const attentionItems =
    memory
      .filter((item) => {
        const openDeadline =
          item.item_type === "task" &&
          item.status === "Open" &&
          item.deadline;

        const pendingApproval =
          item.item_type ===
            "approval" &&
          item.status === "Pending";

        return (
          openDeadline ||
          pendingApproval
        );
      })
      .slice(
        0,
        5
      );


  return (
    <div className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">
            PROJECT OVERVIEW
          </span>

          <h1>
            ProjectPulse AI
          </h1>

          <p>
            Turn communication overload
            into clear project intelligence.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={onAnalyzeClick}
        >
          + Analyze Conversation
        </button>
      </header>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="stat-grid">
        <StatCard
          label="Conversations"
          value={
            stats.conversations
          }
          description="Processed communication"
          symbol="C"
        />

        <StatCard
          label="Open Tasks"
          value={
            stats.open_tasks
          }
          description="Actions requiring attention"
          symbol="T"
        />

        <StatCard
          label="Decisions"
          value={
            stats.decisions
          }
          description="Confirmed decisions captured"
          symbol="D"
        />

        <StatCard
          label="Pending Approvals"
          value={
            stats.pending_approvals
          }
          description="Waiting for confirmation"
          symbol="A"
          warning
        />
      </section>


      <section className="dashboard-grid">
        <div className="panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">
                PROJECT MEMORY
              </span>

              <h2>
                Recent intelligence
              </h2>
            </div>

            <button
              className="refresh-button"
              onClick={
                loadDashboard
              }
            >
              Refresh
            </button>
          </div>


          {loading ? (
            <div className="empty-state">
              Loading project memory...
            </div>
          ) : recentItems.length ===
            0 ? (
            <div className="empty-state">
              <h3>
                No project intelligence yet
              </h3>

              <p>
                Analyze your first
                conversation to populate
                project memory.
              </p>

              <button
                className="secondary-button"
                onClick={
                  onAnalyzeClick
                }
              >
                Analyze conversation
              </button>
            </div>
          ) : (
            <div className="memory-list">
              {recentItems.map(
                (item) => (
                  <MemoryRow
                    key={item.id}
                    item={item}
                    onUpdated={
                      loadDashboard
                    }
                  />
                )
              )}
            </div>
          )}
        </div>


        <div className="panel attention-panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow warning-text">
                ATTENTION NEEDED
              </span>

              <h2>
                Don't let this get buried
              </h2>
            </div>
          </div>


          {attentionItems.length ===
          0 ? (
            <div className="empty-state small">
              <h3>
                You're all caught up
              </h3>

              <p>
                No open deadlines or
                pending approvals.
              </p>
            </div>
          ) : (
            <div className="attention-list">
              {attentionItems.map(
                (item) => (
                  <div
                    className="attention-row"
                    key={item.id}
                  >
                    <div className="attention-icon">
                      !
                    </div>

                    <div className="attention-content">
                      <h3>
                        {item.content}
                      </h3>

                      <p>
                        {item.deadline
                          ? `Deadline: ${item.deadline}`
                          : "Approval still required"}
                      </p>

                      <span>
                        {item.item_type ===
                        "task"
                          ? "Deadline detected"
                          : "Pending approval"}
                      </span>

                      <StatusActionButton
                        item={item}
                        onUpdated={
                          loadDashboard
                        }
                      />
                    </div>
                  </div>
                )
              )}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}


function StatCard({
  label,
  value,
  description,
  symbol,
  warning = false,
}) {
  return (
    <div
      className={
        warning
          ? "stat-card warning-stat"
          : "stat-card"
      }
    >
      <div className="stat-card-top">
        <span>
          {label}
        </span>

        <div
          className={
            warning
              ? "stat-symbol warning-symbol"
              : "stat-symbol"
          }
        >
          {symbol}
        </div>
      </div>

      <strong>
        {value}
      </strong>

      <p>
        {description}
      </p>
    </div>
  );
}


function MemoryRow({
  item,
  onUpdated,
}) {
  return (
    <div className="memory-row">
      <div
        className={
          `type-icon ${item.item_type}`
        }
      >
        {item.item_type
          .charAt(0)
          .toUpperCase()}
      </div>


      <div className="memory-main">
        <h3>
          {item.content}
        </h3>

        <div className="memory-meta">
          <span>
            {item.item_type}
          </span>

          <span>•</span>

          <span>
            {item.source}
          </span>

          {item.responsible && (
            <>
              <span>•</span>

              <span>
                {item.responsible}
              </span>
            </>
          )}

          {item.deadline && (
            <>
              <span>•</span>

              <span>
                {item.deadline}
              </span>
            </>
          )}
        </div>

        <StatusActionButton
          item={item}
          onUpdated={onUpdated}
        />
      </div>


      <span
        className={
          `status-badge ${item.status.toLowerCase()}`
        }
      >
        {item.status}
      </span>
    </div>
  );
}


export default DashboardPage;