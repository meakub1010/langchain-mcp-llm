from langchain_core.messages import trim_messages

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

    old, recent = messages[:-keep_recent], messages[-keep_recent:]
    transcript = "\n".join(f"{m.type}: {m.content}" for m in old if hasattr(m, "content"))

    summary = model.invoke([
        ("system", "Summarize this conversation in 2-3 sentences, keeping any facts, "
                   "numbers, or decisions the user would need remembered."),
        ("user", transcript),
    ])

    return [("system", f"Earlier conversion summary: {summary.content}")] + recent