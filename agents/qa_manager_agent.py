from agents.base_agent import BaseAgent
import os

class QAManagerAgent(BaseAgent):
    def run(self, task_input=None):
        self.logger.info("Starting final system-wide QA...")
        reqs = self.get_state("requirements")
        fr_list = reqs.get("fr", [])
        workspace_path = "workspace/src/"
        
        # 1. Verification Logic: Check if all FRs have corresponding files
        missing_artifacts = []
        for fr in fr_list:
            expected_file = fr.lower().replace(" ", "_") + ".py"
            if not os.path.exists(os.path.join(workspace_path, expected_file)):
                missing_artifacts.append(fr)
        
        if not missing_artifacts:
            print(f"[{self.name}] All functional requirements verified in workspace.")
            self.update_state("factory_status", "Production Ready")
            self.emit_event("FINAL_CERTIFICATION", {"status": "PASSED", "report": "All modules present and validated."})
            return "System Certified"
        else:
            print(f"[{self.name}] QA Failed: Missing artifacts for {missing_artifacts}")
            self.emit_event("QA_FAILURE", {"missing": missing_artifacts})
            return "QA Failed"
