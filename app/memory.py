from langchain_core.messages import trim_messages, ToolMessage
from datetime import date

def trim_history(messages, model, max_tokens=4000):
    return trim_messages(
        messages,
        max_tokens=max_tokens,
        strategy="last",
        token_counter=model,
        start_on="human"
    )

def summarize_if_needed(messages, model, keep_recent=6, trigger_at=14):
    if len(messages) <= trigger_at:
        return messages

    split = len(messages) - keep_recent

    while split > 0 and isinstance(messages[split], ToolMessage):
        split-= 1

    old, recent = messages[:split], messages[split:]

    transcript = "\n".join(f"{m.type}: {m.content}" for m in old if hasattr(m, "content"))

    summary = model.invoke([
        ("system", "Summarize this conversation in 2-3 sentences, keeping any facts, "
                   "numbers, or decisions the user would need remembered."),
        ("user", transcript),
    ])

    date_anchor = (
        "system",
        f"Today's date is {date.today().isoformat()}."
            f"Use this to resolve any relative or partial dates the user mentions"
            f"(e.g. 'next Tuesday', 'Sep 29' with no year) into full, correct dates."
    )
    summary_msg = ("system", f"Earlier conversation summary: {summary.content}")
    return [date_anchor, summary_msg] + recent