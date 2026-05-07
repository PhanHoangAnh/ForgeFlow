from agents.teamlead_agent import TeamLeadAgent
from agents.solution_arch_agent import SolutionArchAgent
from agents.implementer_agent import ImplementerAgent
from agents.devops_agent import DevOpsAgent
from agents.auditor_agent import AuditorAgent
from agents.qa_manager_agent import QAManagerAgent

def run_full_factory_process():
    # Initialize agents
    tl = TeamLeadAgent("TeamLead")
    arch = SolutionArchAgent("SolutionArch")
    impl = ImplementerAgent("Implementer")
    devops = DevOpsAgent("DevOps")
    auditor = AuditorAgent("Auditor")
    qa = QAManagerAgent("QA_Manager")

    print("--- Starting Full Solution Factory Loop ---")
    
    # Get the full list of FRs from the state
    fr_list = tl.get_state("requirements").get("fr", [])
    
    for fr in fr_list:
        print(f"\n>>> Processing Requirement: {fr} <<<")
        
        # 1. TeamLead sets the current requirement
        tl.run() 
        
        # 2. Get the specific requirement details for the architect
        events = arch.get_state("event_queue")
        start_event = [e for e in events if e["type"] == "IMPLEMENTATION_START"][-1]
        blueprint = arch.run(start_event["details"]["requirement"])
        
        # 3. Implementation attempt with Reactive Infrastructure Loop
        result = impl.run(blueprint)
        
        if "Paused" in result:
            print("--- [REACTIVE EVENT] Fixing Environment ---")
            devops.run()
            auditor.run()
            print("--- [REACTIVE EVENT] Resuming ---")
            impl.run(blueprint)
            
        # 4. Mark the requirement as completed in the state for TeamLead tracking
        progress = tl.get_state("implementation_progress") or {}
        target_file = blueprint["target_file"]
        progress[fr] = "Completed"
        tl.update_state("implementation_progress", progress)

    # 5. Final QA Certification
    print("\n--- Starting Final Governance Tier ---")
    qa.run()
    
    final_status = qa.get_state("factory_status")
    print(f"Final Factory Status: {final_status}")

if __name__ == "__main__":
    run_full_factory_process()