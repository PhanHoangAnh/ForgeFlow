import os
from agents.base_agent import BaseAgent

class ImplementerAgent(BaseAgent):
    def run(self, blueprint_details):
        target_file = blueprint_details["target_file"]
        requirement = blueprint_details["requirement"]
        self.logger.info(f"Analyzing implementation for {requirement}")

        # 1. Gather all system context from the specs folder and environment
        specs = self.read_specs()
        env_libs = self.get_state("environment_state")["libs"]
        
        system_prompt = (
            "You are a Senior Polymorphic Developer in the ForgeFlow Factory. "
            "Identify if the current task is Frontend or Backend based on context. "
            "Output ONLY pure, production-ready code. No markdown backticks, no explanations."
        )
        
        user_prompt = (
            f"GOAL: Implement {requirement}\n"
            f"TARGET FILE: {target_file}\n"
            f"BLUEPRINT: {blueprint_details}\n"
            f"ENVIRONMENT LIBS: {env_libs}\n"
            f"SYSTEM CONTEXT (Requirements): {specs}\n\n"
            "If a specific library is missing for this code to work, "
            "start your response with 'DCR_REQUIRED: [lib_name]'."
        )

        # 2. Call the Gemini Brain to generate the solution
        raw_response = self.think(user_prompt, system_instruction=system_prompt)

        # 3. Handle Reactive Dependency Requests
        if "DCR_REQUIRED" in raw_response:
            lib_needed = raw_response.split(":")[1].strip().split()[0]
            self.emit_event("DCR", {
                "library": lib_needed, 
                "reason": "LLM identified library requirement for implementation"
            })
            return "Paused: Waiting for DCR"

        # 4. Persistence Logic
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        # Clean potential markdown backticks if the LLM provided them
        clean_code = raw_response.replace("```python", "").replace("```", "").strip()
        
        with open(target_file, "w") as f:
            f.write(clean_code)
            
        print(f"[{self.name}] Brain-generated code saved to {target_file}")
        self.emit_event("CODE_READY", {"file": target_file})
        return "Code Implemented"