import time
from agents.architecture_agent import ArchitectureAgent
from agents.critic_agent import CriticAgent

def run_requirement_phase():
    gaa = ArchitectureAgent("GAA")
    rca = CriticAgent("RCA")
    
    print("--- Starting Requirement Hardening Phase ---")
    
    # Initial Run
    gaa.run("Build a multi-agent coding factory.")
    
    max_retries = 3
    for i in range(max_retries):
        # Let the Critic check the work
        rca.run()
        
        status = rca.get_state("requirements_status")
        if status == "Approved":
            print("--- Requirements Hardened and Approved ---")
            break
            
        # Check for feedback events
        events = rca.get_state("event_queue")
        pending_feedback = [e for e in events if e["type"] == "REQUIREMENT_FEEDBACK" and e["status"] == "pending"]
        
        if pending_feedback:
            feedback_item = pending_feedback[-1] # Get latest
            print(f"Loop {i+1}: GAA addressing feedback...")
            
            # GAA incorporates feedback (Simulated)
            gaa.update_state("requirements", {
                "fr": ["System authentication", "Agent state management", "Automated environment setup"],
                "nfr": ["Python 3.11+", "Conda for env management", "JSON-based shared state", "Logging system"]
            })
            
            # Mark event as handled
            events[events.index(feedback_item)]["status"] = "resolved"
            rca.update_state("event_queue", events)
        
        time.sleep(1)

if __name__ == "__main__":
    run_requirement_phase()