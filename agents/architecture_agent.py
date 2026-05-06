import os
from agents.base_agent import BaseAgent

class ArchitectureAgent(BaseAgent):
    def run(self, user_prompt):
        # In a real scenario, 'think' would call the LLM
        # For now, we simulate the output decomposition
        self.logger.info("Decomposing requirements...")
        
        # Simulated decomposition based on your project goals
        fr = ["System authentication", "Agent state management", "Automated environment setup"]
        nfr = ["Python 3.11+", "Conda for env management", "JSON-based shared state"]
        
        # 1. Update the shared state
        reqs = self.get_state("requirements")
        reqs["fr"] = fr
        reqs["nfr"] = nfr
        self.update_state("requirements", reqs)
        
        # 2. Generate the spec file
        spec_content = f"# Functional Requirements\n" + "\n".join([f"- {i}" for i in fr])
        spec_content += f"\n\n# Non-Functional Requirements\n" + "\n".join([f"- {i}" for i in nfr])
        
        with open("spec_requirements/requirements.md", "w") as f:
            f.write(spec_content)
            
        print(f"[{self.name}] Specs generated in spec_requirements/requirements.md")
        return "Specs drafted."