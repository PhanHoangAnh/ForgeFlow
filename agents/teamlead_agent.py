from agents.base_agent import BaseAgent

class TeamLeadAgent(BaseAgent):
    def run(self, task_input=None):
        self.logger.info("Orchestrating implementation phase...")
        reqs = self.get_state("requirements")
        fr_list = reqs.get("fr", [])
        
        # Track progress in state if not already there
        progress = self.get_state("implementation_progress") or {}
        
        for fr in fr_list:
            if progress.get(fr) == "Completed":
                continue
            
            print(f"[{self.name}] Next Requirement: {fr}")
            # Emit event to trigger Solution Architect
            self.emit_event("IMPLEMENTATION_START", {"requirement": fr})
            
            # For this prototype step, we only process the first one
            break
            
        return "Implementation Batch Started."
