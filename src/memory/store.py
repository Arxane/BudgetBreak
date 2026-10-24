import uuid
from src.schemas import TrustLevel


class MemoryItem:
    def __init__(self, content: str, trust_level: TrustLevel, session_id: str):
        self.content = content
        self.trust_level = trust_level
        self.session_id = session_id

class MemorySandbox:
    def __init__(self, default_session_id: str = "session_001"):
        self.default_session_id = default_session_id
        self.memories: list[MemoryItem] = []
        self.trust_log: list[dict[str, str]] = []

    def add_item(self, content: str, trust_level: TrustLevel, session_id: str | None = None) -> None:
        sid = session_id or self.default_session_id
        item = MemoryItem(content, trust_level, sid)
        self.memories.append(item)
        self.trust_log.append({
            "content": content,
            "trust_level": trust_level.value,
            "session_id": sid,
        })

    def generate_canary(self) -> str:
        return f"CANARY_{uuid.uuid4().hex[:8]}"

    def build_memory_context(self, session_id: str | None = None) -> str:
        target_id = session_id or self.default_session_id
        relevant_items = [m for m in self.memories if m.session_id == target_id]
        context_blocks = []
        for item in relevant_items:
            context_blocks.append(f"[{item.trust_level.value.upper()}] {item.content}")
        return "\n".join(context_blocks)


    def clear(self) -> None:
        self.memories.clear()
        self.trust_log.clear()
