import os
import json
import logging
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, state_path="state.json"):
        self.name = name
        self.state_path = state_path
        self.log_file = f"logs/{self.name.lower()}.log"
        
        # Setup logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)
        
        # Ensure state file exists
        if not os.path.exists(self.state_path):
            self._write_state({
                "requirements": {"fr": [], "nfr": []},
                "environment_state": {"status": "uninitialized", "libs": []},
                "event_queue": [],
                "project_metadata": {"name": "ForgeFlow_Project", "path": "workspace/"}
            })

    def _read_state(self):
        with open(self.state_path, 'r') as f:
            return json.load(f)

    def _write_state(self, state):
        with open(self.state_path, 'w') as f:
            json.dump(state, f, indent=4)

    def get_state(self, key):
        state = self._read_state()
        return state.get(key)

    def update_state(self, key, value):
        state = self._read_state()
        state[key] = value
        self._write_state(state)
        self.logger.info(f"Updated state: {key}")

    def emit_event(self, event_type, details):
        """Used for DCRs (Dependency Change Requests)"""
        state = self._read_state()
        event = {
            "from": self.name,
            "type": event_type,
            "details": details,
            "status": "pending"
        }
        state["event_queue"].append(event)
        self._write_state(state)
        self.logger.info(f"Emitted event: {event_type}")

    @abstractmethod
    def run(self, task_input):
        """To be implemented by specific agents"""
        pass

    def think(self, prompt):
        # This will be connected to your LLM/Gemini API wrapper
        self.logger.info(f"Thinking about: {prompt[:50]}...")
        print(f"[{self.name}] Processing...")
        # Placeholder for actual LLM call
        return "LLM_RESPONSE_PLACEHOLDER"