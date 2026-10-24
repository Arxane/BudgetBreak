import json
import re
from typing import Any, Dict, Optional, Tuple

from src.schemas import ToolCallTrace


class MockToolSandbox:
    def __init__(self):
        self.execution_history: list[ToolCallTrace] = []
    def parse_and_execute(self, model_output: str) -> Optional[ToolCallTrace]:
        match = re.search(r"TOOL_CALL:\s*(\w+)\((.*?)\)", model_output)
        if not match:
            return None

        tool_name = match.group(1)
        raw_args = match.group(2)

        parsed_args: Dict[str, Any] = {}
        if raw_args.strip():
            for pair in raw_args.split(","):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    parsed_args[k.strip()] = v.strip().strip("'\"")
                else:
                    parsed_args["arg"] = pair.strip()


        trace = ToolCallTrace(tool_name=tool_name, arguments=parsed_args, executed=True)
        self.execution_history.append(trace)
        return trace

    def clear(self) -> None:
        self.execution_history.clear()
