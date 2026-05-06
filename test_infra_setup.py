from agents.devops_agent import DevOpsAgent
from agents.auditor_agent import AuditorAgent

def run_infrastructure_phase():
    devops = DevOpsAgent("DevOps_Lead")
    auditor = AuditorAgent("System_Auditor")
    
    print("--- Starting Infrastructure Phase ---")
    
    # 1. Provision Environment
    devops.run()
    
    # 2. Audit Infrastructure
    auditor.run()
    
    status = auditor.get_state("infrastructure_status")
    if status == "Validated":
        print("--- Infrastructure Tier: READY ---")
    else:
        print("--- Infrastructure Tier: FAILED ---")

if __name__ == "__main__":
    run_infrastructure_phase()
