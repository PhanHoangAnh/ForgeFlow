from agents.teamlead_agent import TeamLeadAgent
from agents.solution_arch_agent import SolutionArchAgent

def run_implementation_batch():
    tl = TeamLeadAgent("TeamLead")
    arch = SolutionArchAgent("SolutionArch")
    
    print("--- Starting Implementation Batch ---")
    
    # 1. TeamLead identifies the next FR
    tl.run()
    
    # 2. Get the latest event to pass to the Architect
    events = tl.get_state("event_queue")
    latest_task = [e for e in events if e["type"] == "IMPLEMENTATION_START"][-1]
    requirement = latest_task["details"]["requirement"]
    
    # 3. Architect generates the blueprint
    arch.run(requirement)
    
    print("--- Batch Hand-off Complete ---")

if __name__ == "__main__":
    run_implementation_batch()
