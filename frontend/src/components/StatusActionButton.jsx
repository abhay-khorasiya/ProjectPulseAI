import {
  useState,
} from "react";

import {
  updateMemoryStatus,
} from "../services/api";


function StatusActionButton({
  item,
  onUpdated,
}) {
  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  if (
    item.item_type === "decision"
  ) {
    return null;
  }


  if (
    item.item_type === "task" &&
    item.status === "Completed"
  ) {
    return (
      <span className="resolved-label">
        ✓ Completed
      </span>
    );
  }


  if (
    item.item_type === "approval" &&
    item.status === "Approved"
  ) {
    return (
      <span className="resolved-label">
        ✓ Approved
      </span>
    );
  }


  let nextStatus = "";
  let label = "";


  if (
    item.item_type === "task" &&
    item.status === "Open"
  ) {
    nextStatus = "Completed";
    label = "Mark Complete";
  }


  if (
    item.item_type === "approval" &&
    item.status === "Pending"
  ) {
    nextStatus = "Approved";
    label = "Mark Approved";
  }


  if (!nextStatus) {
    return null;
  }


  async function handleUpdate() {
    setLoading(true);
    setError("");

    try {
      await updateMemoryStatus(
        item.id,
        nextStatus
      );

      if (onUpdated) {
        await onUpdated();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="status-action-wrapper">
      <button
        type="button"
        className="status-action-button"
        onClick={handleUpdate}
        disabled={loading}
      >
        {loading
          ? "Updating..."
          : label}
      </button>

      {error && (
        <span className="status-action-error">
          {error}
        </span>
      )}
    </div>
  );
}


export default StatusActionButton;