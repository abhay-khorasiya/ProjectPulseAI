import {
  useState,
} from "react";

import AnalysisResults
  from "../components/AnalysisResults";

import {
  analyzeAndSaveConversation,
} from "../services/api";


const SAMPLE_CONVERSATION = `Rahul: Client approved Italian marble for the lobby.
Priya: Abhay, please update the material schedule by Friday.
Abhay: Sure, I will update it.
Rahul: Abhay, please confirm supplier availability before 15 September.
Priya: Bathroom tiles are still pending approval.`;


function AnalyzePage() {
  const [source, setSource] =
    useState("WhatsApp");

  const [text, setText] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function handleAnalyze(event) {
    event.preventDefault();

    if (!text.trim()) {
      setError(
        "Please enter a project conversation."
      );

      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data =
        await analyzeAndSaveConversation(
          source,
          text.trim()
        );

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  function loadSample() {
    setSource("WhatsApp");
    setText(SAMPLE_CONVERSATION);
    setResult(null);
    setError("");
  }


  function clearConversation() {
    setText("");
    setResult(null);
    setError("");
  }


  return (
    <div className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">
            INTELLIGENT PROCESSING
          </span>

          <h1>
            Analyze Conversation
          </h1>

          <p>
            Transform unstructured project
            communication into structured,
            actionable information.
          </p>
        </div>
      </header>


      <section className="analyze-layout">
        <div className="panel input-panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">
                COMMUNICATION INPUT
              </span>

              <h2>
                Paste project communication
              </h2>
            </div>

            <button
              className="text-button"
              type="button"
              onClick={loadSample}
            >
              Load sample
            </button>
          </div>


          <form onSubmit={handleAnalyze}>
            <label className="form-label">
              Communication Source
            </label>

            <select
              className="form-control"
              value={source}
              onChange={(event) =>
                setSource(
                  event.target.value
                )
              }
            >
              <option value="WhatsApp">
                WhatsApp
              </option>

              <option value="Email">
                Email
              </option>

              <option value="Meeting Notes">
                Meeting Notes
              </option>

              <option value="Transcript">
                Transcript
              </option>

              <option value="Other">
                Other
              </option>
            </select>


            <label className="form-label conversation-label">
              Conversation / Notes
            </label>

            <textarea
              className="conversation-input"
              placeholder={`Example:

Rahul: Client approved the lobby marble.
Priya: Abhay, please update the material schedule by Friday.
Client: Bathroom tiles are still pending approval.`}
              value={text}
              onChange={(event) =>
                setText(
                  event.target.value
                )
              }
            />


            <div className="input-footer">
              <span>
                {text.length} characters
              </span>

              <div className="input-actions">
                <button
                  type="button"
                  className="secondary-button"
                  onClick={
                    clearConversation
                  }
                >
                  Clear
                </button>

                <button
                  type="submit"
                  className="primary-button"
                  disabled={loading}
                >
                  {loading
                    ? "Analyzing..."
                    : "✦ Analyze & Save"}
                </button>
              </div>
            </div>
          </form>


          {error && (
            <div className="error-box">
              {error}
            </div>
          )}
        </div>


        <div className="analysis-info">
          <div className="info-card">
            <span className="eyebrow">
              HOW IT WORKS
            </span>

            <h3>
              Communication → Intelligence
            </h3>

            <p>
              ProjectPulse processes
              communication locally and extracts
              important project information.
            </p>

            <div className="process-list">
              <div>
                <span>1</span>
                Conversation capture
              </div>

              <div>
                <span>2</span>
                Action extraction
              </div>

              <div>
                <span>3</span>
                Responsibility detection
              </div>

              <div>
                <span>4</span>
                Deadline detection
              </div>

              <div>
                <span>5</span>
                Decisions & approvals
              </div>

              <div>
                <span>6</span>
                Searchable memory
              </div>
            </div>
          </div>


          <div className="privacy-card">
            <strong>
              ₹0 Local Intelligence
            </strong>

            <p>
              No paid AI API is required for
              the current processing pipeline.
            </p>
          </div>
        </div>
      </section>


      {result && (
        <AnalysisResults
          result={result}
        />
      )}
    </div>
  );
}


export default AnalyzePage;