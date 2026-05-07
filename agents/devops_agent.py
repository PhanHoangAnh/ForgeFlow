import os
from agents.base_agent import BaseAgent

class DevOpsAgent(BaseAgent):
    def run(self, task_input=None):
        self.logger.info("Checking for infrastructure tasks...")
        events = self.get_state("event_queue")
        
        # 1. Check for Reactive Tasks (DCRs)
        pending_dcrs = [e for e in events if e["type"] == "DCR" and e["status"] == "pending"]
        
        if pending_dcrs:
            print(f"[{self.name}] Reactive Mode: Addressing Dependency Change Requests...")
            env_state = self.get_state("environment_state")
            
            for dcr in pending_dcrs:
                lib = dcr["details"]["library"]
                reason = dcr["details"]["reason"]
                print(f"[{self.name}] Installing '{lib}' ({reason})...")
                
                # Update local environment state
                if lib not in env_state["libs"]:
                    env_state["libs"].append(lib)
                
                # Mark the specific event as resolved in our local list
                dcr["status"] = "resolved"
            
            # Commit updates to state
            self.update_state("environment_state", env_state)
            self.update_state("event_queue", events)
            print(f"[{self.name}] Environment updated and DCRs resolved.")
            return "Dependencies Updated"

        # 2. Initial Provisioning Logic (Fallback)
        print(f"[{self.name}] No pending DCRs. Ensuring base infrastructure...")
        # ... (Keep your initial environment.yml logic here)
        return "Base Infrastructure Verified"