import json
import re


# ------------------------------------------------------------
# ProjectPulse AI
# Free Local Conversation Intelligence Engine
# ------------------------------------------------------------


TASK_KEYWORDS = [
    "please",
    "need to",
    "needs to",
    "must",
    "should",
    "have to",
    "update",
    "confirm",
    "send",
    "prepare",
    "review",
    "check",
    "complete",
    "submit",
    "share",
    "ask",
    "follow up",
    "finalize",
    "schedule",
    "arrange",
    "provide",
    "upload",
    "call",
    "contact",
]


DECISION_KEYWORDS = [
    "approved",
    "approve",
    "decided",
    "decision",
    "confirmed",
    "agreed",
    "finalized",
    "selected",
    "accepted",
]


PENDING_APPROVAL_KEYWORDS = [
    "pending approval",
    "awaiting approval",
    "waiting for approval",
    "needs approval",
    "need approval",
    "not yet approved",
    "approval pending",
]


# ------------------------------------------------------------
# Text Cleaning
# ------------------------------------------------------------

def clean_text(text):
    """
    Clean unnecessary spaces while keeping
    the conversation readable.
    """

    text = text.strip()

    text = re.sub(
        r"\r\n",
        "\n",
        text
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    return text


# ------------------------------------------------------------
# Split Conversation
# ------------------------------------------------------------

def split_conversation(text):
    """
    Split communication into individual statements.

    Supports:
    - WhatsApp messages
    - Email text
    - Meeting notes
    - Plain text conversations
    """

    text = clean_text(text)

    parts = re.split(
        r"(?<=[.!?])\s+|\n+",
        text
    )

    statements = []

    for part in parts:
        part = part.strip()

        if part:
            statements.append(part)

    return statements


# ------------------------------------------------------------
# Speaker Detection
# ------------------------------------------------------------

def get_speaker(statement):
    """
    Detect speaker from text such as:

    Rahul: Please send the drawing.
    Priya: Client approved the marble.
    """

    match = re.match(
        r"^([A-Za-z][A-Za-z .'-]{0,40}):\s*(.+)$",
        statement
    )

    if match:
        speaker = match.group(1).strip()
        content = match.group(2).strip()

        return speaker, content

    return None, statement.strip()


# ------------------------------------------------------------
# Acknowledgement Detection
# ------------------------------------------------------------

def is_acknowledgement(text):
    """
    Detect short replies that acknowledge an already
    assigned task instead of creating a new task.

    Example:
    Sure, I will update it.

    This should not become another task.
    """

    cleaned = text.strip().lower()

    cleaned_without_punctuation = re.sub(
        r"[.!?]+$",
        "",
        cleaned
    ).strip()

    simple_acknowledgements = {
        "ok",
        "okay",
        "sure",
        "done",
        "noted",
        "got it",
        "will do",
        "sounds good",
        "understood",
        "thanks",
        "thank you",
    }

    if cleaned_without_punctuation in simple_acknowledgements:
        return True

    words = cleaned_without_punctuation.split()

    # Example:
    # Sure, I will update it.
    # Okay, I will do that.
    if len(words) <= 10:
        starts_like_acknowledgement = any(
            cleaned_without_punctuation.startswith(prefix)
            for prefix in [
                "sure",
                "okay",
                "ok",
                "got it",
                "noted",
                "yes",
                "yep",
            ]
        )

        contains_generic_reference = re.search(
            r"\b(it|that|this)\b",
            cleaned_without_punctuation
        )

        contains_commitment = re.search(
            r"\b(i will|i'll|i can|will do)\b",
            cleaned_without_punctuation
        )

        if (
            starts_like_acknowledgement
            and contains_generic_reference
            and contains_commitment
        ):
            return True

    return False


# ------------------------------------------------------------
# Deadline Detection
# ------------------------------------------------------------

def extract_deadline(text):
    """
    Extract common project deadline expressions.
    """

    patterns = [
        r"\bby\s+(today|tomorrow|tonight)\b",

        r"\bbefore\s+(today|tomorrow|tonight)\b",

        r"\bby\s+"
        r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",

        r"\bbefore\s+"
        r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",

        r"\bnext\s+"
        r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",

        r"\bby\s+\d{1,2}(?:st|nd|rd|th)?\s+"
        r"(?:january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\b",

        r"\bbefore\s+\d{1,2}(?:st|nd|rd|th)?\s+"
        r"(?:january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\b",

        r"\bon\s+\d{1,2}(?:st|nd|rd|th)?\s+"
        r"(?:january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\b",

        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

        r"\b\d{4}-\d{2}-\d{2}\b",

        r"\bEOD\b",

        r"\bend of day\b",

        r"\bend of this week\b",

        r"\bnext week\b",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:
            return match.group(0)

    return None


# ------------------------------------------------------------
# Responsible Person Detection
# ------------------------------------------------------------

def extract_responsible_person(
    statement,
    speaker=None
):
    """
    Identify who is expected to perform an action.
    """

    # Example:
    # Abhay, please update the schedule.
    match = re.search(
        r"\b([A-Z][A-Za-z'-]+),\s*"
        r"(?:please\s+)?"
        r"(?:update|confirm|send|prepare|review|check|complete|"
        r"submit|share|ask|finalize|schedule|arrange|provide|"
        r"upload|call|contact)",
        statement
    )

    if match:
        return match.group(1)

    # Example:
    # Abhay should update the schedule.
    match = re.search(
        r"\b([A-Z][A-Za-z'-]+)\s+"
        r"(?:should|must|needs to|need to|has to|will)\b",
        statement
    )

    if match:
        return match.group(1)

    # Example:
    # Assigned to Abhay
    match = re.search(
        r"\bassigned to\s+([A-Z][A-Za-z'-]+)",
        statement,
        flags=re.IGNORECASE
    )

    if match:
        return match.group(1)

    # Example:
    # Abhay: I will prepare the report.
    if speaker:
        self_assignment = re.search(
            r"\bI\s+(?:will|shall|can)\s+"
            r"(?:prepare|send|review|update|confirm|check|"
            r"complete|submit|share|finalize|schedule|"
            r"arrange|provide|upload|call|contact)\b",
            statement,
            flags=re.IGNORECASE
        )

        if self_assignment:
            return speaker

    return "Unassigned"


# ------------------------------------------------------------
# Task Detection
# ------------------------------------------------------------

def is_task(statement):
    """
    Determine whether text contains a meaningful action.
    """

    if is_acknowledgement(statement):
        return False

    lower_text = statement.lower()

    return any(
        keyword in lower_text
        for keyword in TASK_KEYWORDS
    )


# ------------------------------------------------------------
# Task Extraction
# ------------------------------------------------------------

def extract_tasks(statements):
    """
    Extract:
    - Action
    - Responsible person
    - Deadline
    - Status
    """

    tasks = []

    seen = set()

    for statement in statements:
        speaker, content = get_speaker(
            statement
        )

        if not is_task(content):
            continue

        normalized = content.lower().strip()

        if normalized in seen:
            continue

        seen.add(normalized)

        responsible = extract_responsible_person(
            content,
            speaker
        )

        deadline = extract_deadline(
            content
        )

        tasks.append(
            {
                "task": content,
                "responsible": responsible,
                "deadline": deadline,
                "status": "Open",
            }
        )

    return tasks


# ------------------------------------------------------------
# Decision Extraction
# ------------------------------------------------------------

def extract_decisions(statements):
    """
    Extract confirmed decisions and approvals.
    """

    decisions = []

    seen = set()

    for statement in statements:
        _, content = get_speaker(
            statement
        )

        lower_text = content.lower()

        # Pending approval is NOT a confirmed decision.
        if any(
            keyword in lower_text
            for keyword in PENDING_APPROVAL_KEYWORDS
        ):
            continue

        if any(
            keyword in lower_text
            for keyword in DECISION_KEYWORDS
        ):
            normalized = content.lower().strip()

            if normalized in seen:
                continue

            seen.add(normalized)

            decisions.append(
                {
                    "decision": content,
                    "status": "Confirmed",
                }
            )

    return decisions


# ------------------------------------------------------------
# Pending Approval Extraction
# ------------------------------------------------------------

def extract_approvals(statements):
    """
    Extract items waiting for approval.
    """

    approvals = []

    seen = set()

    for statement in statements:
        _, content = get_speaker(
            statement
        )

        lower_text = content.lower()

        if any(
            keyword in lower_text
            for keyword in PENDING_APPROVAL_KEYWORDS
        ):
            normalized = content.lower().strip()

            if normalized in seen:
                continue

            seen.add(normalized)

            approvals.append(
                {
                    "item": content,
                    "status": "Pending",
                }
            )

    return approvals


# ------------------------------------------------------------
# Summary Generation
# ------------------------------------------------------------

def generate_summary(
    statements,
    tasks,
    decisions,
    approvals
):
    """
    Create a concise local summary.

    Priority:
    1. Decisions
    2. Tasks
    3. Pending approvals

    Acknowledgement messages are ignored.
    """

    summary_items = []

    # Add important decisions first.
    for decision in decisions:
        text = decision["decision"]

        if text not in summary_items:
            summary_items.append(text)

    # Add important actions.
    for task in tasks:
        text = task["task"]

        if text not in summary_items:
            summary_items.append(text)

    # Add pending approvals.
    for approval in approvals:
        text = approval["item"]

        if text not in summary_items:
            summary_items.append(text)

    # Fallback when no structured information is detected.
    if not summary_items:
        for statement in statements:
            _, content = get_speaker(
                statement
            )

            if is_acknowledgement(content):
                continue

            if content not in summary_items:
                summary_items.append(content)

            if len(summary_items) >= 3:
                break

    if not summary_items:
        return (
            "No meaningful project information "
            "was detected."
        )

    # Keep summary concise.
    summary_items = summary_items[:4]

    return " ".join(summary_items)


# ------------------------------------------------------------
# Attention Needed
# ------------------------------------------------------------

def build_attention_items(
    tasks,
    approvals
):
    """
    Highlight information which could easily
    get buried in project communication.
    """

    attention = []

    # Tasks with deadlines need attention.
    for task in tasks:
        if task["deadline"]:
            attention.append(
                {
                    "type": "Deadline",
                    "message": task["task"],
                    "detail": task["deadline"],
                }
            )

    # Pending approvals need attention.
    for approval in approvals:
        attention.append(
            {
                "type": "Pending Approval",
                "message": approval["item"],
                "detail": "Approval still required",
            }
        )

    return attention


# ------------------------------------------------------------
# Main Analyzer
# ------------------------------------------------------------

def analyze_conversation(text):
    """
    Main ProjectPulse intelligence pipeline.

    Converts unstructured communication into:

    - Summary
    - Tasks
    - Responsible people
    - Deadlines
    - Decisions
    - Pending approvals
    - Attention items
    """

    statements = split_conversation(
        text
    )

    tasks = extract_tasks(
        statements
    )

    decisions = extract_decisions(
        statements
    )

    approvals = extract_approvals(
        statements
    )

    summary = generate_summary(
        statements,
        tasks,
        decisions,
        approvals
    )

    attention = build_attention_items(
        tasks,
        approvals
    )

    return {
        "summary": summary,
        "tasks": tasks,
        "decisions": decisions,
        "approvals": approvals,
        "attention_needed": attention,
    }


# ------------------------------------------------------------
# Local Testing
# ------------------------------------------------------------

if __name__ == "__main__":

    sample_conversation = """
Rahul: Client approved Italian marble for the lobby.
Priya: Abhay, please update the material schedule by Friday.
Abhay: Sure, I will update it.
Rahul: Abhay, please confirm supplier availability before 15 September.
Priya: Bathroom tiles are still pending approval.
"""

    result = analyze_conversation(
        sample_conversation
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )