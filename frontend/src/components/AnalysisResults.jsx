import {
  useState,
} from "react";

import {
  downloadTextReport,
} from "../utils/reportExport";

import "../styles/results.css";


function AnalysisResults({
  result,
}) {
  const [copied, setCopied] =
    useState(false);


  async function copySummary() {
    try {
      await navigator.clipboard.writeText(
        result.summary
      );

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 1800);
    } catch {
      setCopied(false);
    }
  }


  return (
    <section className="results-section">
      <div className="success-banner">
        <div>
          <strong>
            Analysis complete
          </strong>

          <p>
            Conversation #
            {result.conversation_id}
            {" "}
            was analyzed and saved to
            Project Memory.
          </p>
        </div>

        <span>
          {result.memory_items_created}
          {" "}
          memory items created
        </span>
      </div>


      <div className="summary-card">
        <div className="summary-header">
          <div>
            <span className="eyebrow">
              INTELLIGENT SUMMARY
            </span>

            <h2>
              Conversation Summary
            </h2>
          </div>

          <div className="report-actions">
            <button
              type="button"
              className="report-button"
              onClick={copySummary}
            >
              {copied
                ? "✓ Copied"
                : "Copy Summary"}
            </button>

            <button
              type="button"
              className="report-button primary-report"
              onClick={() =>
                downloadTextReport(result)
              }
            >
              Download Report
            </button>
          </div>
        </div>

        <p>{result.summary}</p>
      </div>


      <div className="result-grid">
        <ResultPanel
          title="Action Items"
          count={result.tasks.length}
        >
          {result.tasks.length === 0 ? (
            <EmptyResult
              text="No action items detected."
            />
          ) : (
            result.tasks.map(
              (task, index) => (
                <div
                  className="result-item"
                  key={`${task.task}-${index}`}
                >
                  <div className="result-number">
                    {index + 1}
                  </div>

                  <div className="result-content">
                    <h3>
                      {task.task}
                    </h3>

                    <div className="result-tags">
                      <span>
                        Responsible:
                        {" "}
                        {task.responsible}
                      </span>

                      {task.deadline && (
                        <span className="deadline-tag">
                          {task.deadline}
                        </span>
                      )}

                      <span>
                        {task.status}
                      </span>
                    </div>
                  </div>
                </div>
              )
            )
          )}
        </ResultPanel>


        <ResultPanel
          title="Decisions"
          count={result.decisions.length}
        >
          {result.decisions.length === 0 ? (
            <EmptyResult
              text="No confirmed decisions detected."
            />
          ) : (
            result.decisions.map(
              (decision, index) => (
                <div
                  className="result-item"
                  key={`${decision.decision}-${index}`}
                >
                  <div className="result-number decision">
                    ✓
                  </div>

                  <div className="result-content">
                    <h3>
                      {decision.decision}
                    </h3>

                    <span className="confirmed-text">
                      {decision.status}
                    </span>
                  </div>
                </div>
              )
            )
          )}
        </ResultPanel>


        <ResultPanel
          title="Pending Approvals"
          count={result.approvals.length}
        >
          {result.approvals.length === 0 ? (
            <EmptyResult
              text="No pending approvals detected."
            />
          ) : (
            result.approvals.map(
              (approval, index) => (
                <div
                  className="result-item"
                  key={`${approval.item}-${index}`}
                >
                  <div className="result-number approval">
                    !
                  </div>

                  <div className="result-content">
                    <h3>
                      {approval.item}
                    </h3>

                    <span className="pending-text">
                      {approval.status}
                    </span>
                  </div>
                </div>
              )
            )
          )}
        </ResultPanel>


        <ResultPanel
          title="Attention Needed"
          count={
            result.attention_needed.length
          }
          warning
        >
          {result.attention_needed.length === 0 ? (
            <EmptyResult
              text="Nothing currently requires urgent attention."
            />
          ) : (
            result.attention_needed.map(
              (item, index) => (
                <div
                  className="result-item"
                  key={`${item.message}-${index}`}
                >
                  <div className="result-number approval">
                    !
                  </div>

                  <div className="result-content">
                    <h3>
                      {item.message}
                    </h3>

                    <div className="result-tags">
                      <span>
                        {item.type}
                      </span>

                      <span className="deadline-tag">
                        {item.detail}
                      </span>
                    </div>
                  </div>
                </div>
              )
            )
          )}
        </ResultPanel>
      </div>
    </section>
  );
}


function ResultPanel({
  title,
  count,
  children,
  warning = false,
}) {
  return (
    <div
      className={
        warning
          ? "panel result-panel warning-result"
          : "panel result-panel"
      }
    >
      <div className="result-panel-title">
        <h2>{title}</h2>

        <span>{count}</span>
      </div>

      {children}
    </div>
  );
}


function EmptyResult({
  text,
}) {
  return (
    <div className="empty-result">
      {text}
    </div>
  );
}


export default AnalysisResults;