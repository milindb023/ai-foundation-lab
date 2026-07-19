class BaseMemoryAgent:
    """Base class for agent memory wrapper variations."""
    def __init__(self, agent, llm):
        self.agent = agent
        self.llm = llm

    def ask(self, question: str) -> str:
        raise NotImplementedError("Subclasses must implement the ask method.")

    def clear(self):
        raise NotImplementedError("Subclasses must implement the clear method.")


class FullHistoryAgent(BaseMemoryAgent):
    """Variation 1: Retain complete conversation history."""
    def __init__(self, agent, llm):
        super().__init__(agent, llm)
        self.chat_history = []

    def ask(self, question: str) -> str:
        messages = self.chat_history + [{"role": "user", "content": question}]
        result = self.agent.invoke({"messages": messages})
        self.chat_history = result["messages"]
        return self.chat_history[-1].content

    def clear(self):
        self.chat_history = []
        print("✅ Complete chat history cleared")


class SlidingWindowAgent(BaseMemoryAgent):
    """Variation 2: Retain only a sliding window of the last N messages."""
    def __init__(self, agent, llm, max_messages: int = 10):
        super().__init__(agent, llm)
        self.chat_history = []
        self.max_messages = max_messages

    def ask(self, question: str) -> str:
        recent_messages = self.chat_history[-self.max_messages:]
        messages = recent_messages + [{"role": "user", "content": question}]
        
        result = self.agent.invoke({"messages": messages})
        self.chat_history = result["messages"][-self.max_messages:]
        return self.chat_history[-1].content

    def clear(self):
        self.chat_history = []
        print(f"✅ Last-{self.max_messages} chat history cleared")


class SummaryWindowAgent(BaseMemoryAgent):
    """Variation 3: Summarize older history and retain last N messages intact."""
    def __init__(self, agent, llm, window_size: int = 10):
        super().__init__(agent, llm)
        self.chat_history = []
        self.summary_text = ""
        self.window_size = window_size

    def _message_to_text(self, message):
        """Helper to serialize messages into readable text format for prompt ingestion."""
        role = getattr(message, "type", None) or getattr(message, "role", None)
        content = getattr(message, "content", None)
        if content is None and isinstance(message, dict):
            role = message.get("role", "message")
            content = message.get("content", "")
        return f"{role}: {content}"

    def _update_summary(self, messages_to_summarize):
        """Invokes LLM to summarize older portion of the conversation."""
        conversation_text = "\n".join(self._message_to_text(m) for m in messages_to_summarize)
        summary_prompt = f"""
You maintain a concise conversation memory.

Existing summary:
{self.summary_text or 'No previous summary.'}

New conversation messages:
{conversation_text}

Create an updated concise summary. Preserve important facts, user preferences,
questions, tool findings, and unresolved tasks. Do not add new information.
"""
        response = self.llm.invoke(summary_prompt)
        self.summary_text = response.content

    def ask(self, question: str) -> str:
        # Pre-execution: check if history window has overflowed
        if len(self.chat_history) > self.window_size:
            older_messages = self.chat_history[:-self.window_size]
            self._update_summary(older_messages)
            self.chat_history = self.chat_history[-self.window_size:]

        messages = []
        if self.summary_text:
            messages.append({
                "role": "system",
                "content": f"Conversation summary from earlier messages:\n{self.summary_text}"
            })
        messages.extend(self.chat_history[-self.window_size:])
        messages.append({"role": "user", "content": question})

        result = self.agent.invoke({"messages": messages})
        returned_messages = result["messages"]
        
        # If a summary was appended, strip it out from stored history to avoid duplicating
        if self.summary_text and returned_messages:
            returned_messages = returned_messages[1:]

        self.chat_history = returned_messages

        # Post-execution: check if latest turn pushed the history over the window
        if len(self.chat_history) > self.window_size:
            older_messages = self.chat_history[:-self.window_size]
            self._update_summary(older_messages)
            self.chat_history = self.chat_history[-self.window_size:]

        return self.chat_history[-1].content

    def clear(self):
        self.summary_text = ""
        self.chat_history = []
        print("✅ Summary and recent chat history cleared")
