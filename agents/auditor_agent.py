from agents.base_agent import BaseAgent

class AuditorAgent(BaseAgent):
    def run(self, task_input=None):
        self.logger.info("Auditing environment state...")
        env_state = self.get_state("environment_state")
        
        # Validation Logic
        is_provisioned = env_state.get("status") == "provisioned"
        has_python = "python_version" in env_state
        
        if is_provisioned and has_python:
            print(f"[{self.name}] Audit Passed: Environment '{env_state['env_name']}' is valid.")
            self.update_state("infrastructure_status", "Validated")
            return "Audit Successful"
        else:
            self.logger.error("Audit failed: Environment not fully provisioned.")
            print(f"[{self.name}] Audit Failed: Incomplete infrastructure.")
            return "Audit Failed"