from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List

class TrustLevel(str, Enum):
    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"
    SYSTEM = "system_controlled"

class AttackFamily(str, Enum):
    INSTRUCTION_INTEGRITY = "instruction_integrity"
    SYNTHETIC_SECRET = "synthetic_secret_disclosure"
    CROSS_SESSION = "cross_session_peristence"

class Scenario(BaseModel):
    id: str
    family: AttackFamily
    system_prompt: str
    user_prompt: str
    untrusted_payload: Optional[str] = None
    canary_token: Optional[str] = None
    forbidden_tool_call: Optional[str] = None
    max_query_budget: int = 1
    max_token_budget: int = 512

class BudgetTracker(BaseModel):
    model_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    wall_time_seconds: float = 0.0

class ToolCallTrace(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    executed: bool = False

class TrialResult(BaseModel):
    scenario_id: str
    is_control: bool
    model_name: str
    raw_output: str
    budget: BudgetTracker

    canary_exposed: bool = False
    unauthorized_action_executed: bool = False
    benign_task_success: bool = False
    false_refusal: bool = False

    tool_traces: List[ToolCallTrace] = Field(default_factory=list)
    trust_log: List[Dict[str, str]] = Field(default_factory=list)
    

