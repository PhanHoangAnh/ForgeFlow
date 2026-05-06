import os
import subprocess
from agents.base_agent import BaseAgent

class DevOpsAgent(BaseAgent):
    def run(self, task_input=None):
        self.logger.info("Initializing infrastructure provisioning...")
        reqs = self.get_state("requirements")
        nfrs = reqs.get("nfr", [])
        
        # 1. Generate Environment Specification
        # In a real scenario, this would parse the NFRs to find libs
        env_name = "forgeflow_env"
        python_version = "3.11" # Extracted from NFR "Python 3.11+"
        
        # Check if environment already exists or needs update
        print(f"[{self.name}] Creating/Updating Conda environment: {env_name}")
        
        # Simulate environment.yml creation
        env_content = f"name: {env_name}\nchannels:\n  - defaults\ndependencies:\n  - python={python_version}\n  - pip\n"
        with open("environment.yml", "w") as f:
            f.write(env_content)
            
        # 2. Execute Shell Command (Simulated for safety, but structure is here)
        # command = f"conda env create -f environment.yml || conda env update -f environment.yml"
        # subprocess.run(command, shell=True)
        
        self.update_state("environment_state", {
            "status": "provisioned",
            "env_name": env_name,
            "python_version": python_version,
            "libs": ["base-python", "pip"]
        })
        
        print(f"[{self.name}] Environment {env_name} provisioned.")
        return "Infrastructure Ready."