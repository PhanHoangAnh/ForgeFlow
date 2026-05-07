import os
import json
import logging
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()

class BaseAgent(ABC):
    def __init__(self, name, state_path="state.json"):
        self.name = name
        self.state_path = state_path
        self.log_file = f"logs/{self.name.lower()}.log"
        
        # 1. Initialize Gemini Client using the .env key
        api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash"

        # Setup logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)
        
        if not os.path.exists(self.state_path):
            self._write_state({
                "requirements": {"fr": [], "nfr": []},
                "environment_state": {"status": "uninitialized", "libs": []},
                "implementation_progress": {},
                "event_queue": [],
                "project_metadata": {"name": "ForgeFlow_Project", "path": "workspace/"}
            })

    def read_specs(self, folder="spec_requirements"):
        """Utility to read all requirement context for the LLM."""
        context = ""
        if not os.path.exists(folder):
            return "No specifications found."
        for filename in os.listdir(folder):
            if filename.endswith(".md"):
                with open(os.path.join(folder, filename), 'r') as f:
                    context += f"\n--- {filename} ---\n{f.read()}\n"
        return context

    def think(self, prompt, system_instruction="You are a senior engineer."):
        """Invokes the Gemini 2.0 Brain."""
        self.logger.info(f"Invoking LLM for {self.name}")
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={'system_instruction': system_instruction}
            )
            return response.text
        except Exception as e:
            self.logger.error(f"LLM Error: {e}")
            return f"Error: {e}"

    def _read_state(self):
        with open(self.state_path, 'r') as f:
            return json.load(f)

    def _write_state(self, state):
        with open(self.state_path, 'w') as f:
            json.dump(state, f, indent=4)

    def get_state(self, key):
        return self._read_state().get(key)

    def update_state(self, key, value):
        state = self._read_state()
        state[key] = value
        self._write_state(state)

    def emit_event(self, event_type, details):
        state = self._read_state()
        event = {"from": self.name, "type": event_type, "details": details, "status": "pending"}
        state["event_queue"].append(event)
        self._write_state(state)