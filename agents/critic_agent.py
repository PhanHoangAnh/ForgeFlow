from agents.base_agent import BaseAgent

class CriticAgent(BaseAgent):
    def run(self, task_input=None):
        self.logger.info("Critiquing requirements...")
        
        # Read what the GAA just did
        reqs = self.get_state("requirements")
        
        # Simulated critique: Identifying a missing NFR
        feedback = []
        if "Logging system" not in str(reqs):
             feedback.append("Missing NFR: Define a centralized logging retention policy.")
        
        if feedback:
            self.emit_event("REQUIREMENT_FEEDBACK", {"critique": feedback})
            print(f"[{self.name}] Feedback issued: {feedback}")
            return "Feedback provided."
        else:
            self.update_state("requirements_status", "Approved")
            print(f"[{self.name}] Requirements approved.")
            return "Approved."