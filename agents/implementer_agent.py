import os
from agents.base_agent import BaseAgent

class ImplementerAgent(BaseAgent):
    def run(self, blueprint_details):
        target_file = blueprint_details["target_file"]
        requirement = blueprint_details["requirement"]
        self.logger.info(f"Analyzing implementation for {requirement}")

        # 1. Gather all system context from the specs folder
        specs = self.read_specs()
        env_libs = self.get_state("environment_state")["libs"]
        
        system_prompt = (
            "You are a Senior Polymorphic Developer in the ForgeFlow Factory. "
            "Identify if the task is Frontend or Backend. "
            "Output ONLY pure code. No markdown backticks, no explanations."
        )
        
        user_prompt = (
            f"GOAL: Implement {requirement}\n"
            f"TARGET FILE: {target_file}\n"
            f"BLUEPRINT: {blueprint_details}\n"
            f"ENVIRONMENT LIBS: {env_libs}\n"
            f"SYSTEM CONTEXT: {specs}\n\n"
            "If a library is missing for this code to work, start with 'DCR_REQUIRED: [lib_name]'."
        )

        # 2. Call the Gemini Brain
        raw_response = self.think(user_prompt, system_instruction=system_prompt)

        # 3. Handle Dependency Requests
        if "DCR_REQUIRED" in raw_response:
            lib_needed = raw_response.split(":")[1].strip().split()[0]
            self.emit_event("DCR", {"library": lib_needed, "reason": "LLM code requirement"})
            return "Paused: Waiting for DCR"

        # 4. Save and Finish
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        # Force-clean code if the LLM provided markdown formatting
        clean_code = raw_response.replace("```python", "").replace("```", "").strip()
        
        with open(target_file, "w") as f:
            f.write(clean_code)
            
        print(f"[{self.name}] Brain-generated code saved to {target_file}")
        self.emit_event("CODE_READY", {"file": target_file})
        return "Code Implemented"