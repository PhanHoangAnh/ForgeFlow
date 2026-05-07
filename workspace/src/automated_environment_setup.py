import os
import json
import subprocess

class AutomatedEnvironmentSetup:

    def __init__(self, config_path="env_config.json", state_path="agent_state.json"):
        """
        Initializes the AutomatedEnvironmentSetup with configuration and state file paths.
        """
        self.config_path = config_path
        self.state_path = state_path
        self.config = self._load_config()
        self.state = self._load_state()

    def _load_config(self):
        """
        Loads environment configuration from a JSON file.
        """
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file not found at {self.config_path}. Using default configuration.")
            return {}  # Or raise an exception if config is mandatory
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.config_path}.  Using default configuration.")
            return {}

    def _load_state(self):
        """
        Loads agent state from a JSON file.
        """
        try:
            with open(self.state_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"State file not found at {self.state_path}.  Initializing with empty state.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.state_path}. Initializing with empty state.")
            return {}


    def process(self):
        """
        Orchestrates the environment setup process.
        """
        self.log_status("Starting environment setup...")

        env_name = self.config.get("env_name", "default_env")
        conda_dependencies = self.config.get("conda_dependencies", [])
        pip_dependencies = self.config.get("pip_dependencies", [])

        if not self.check_env_exists(env_name):
            self.create_env(env_name)
        else:
            self.log_status(f"Environment '{env_name}' already exists.")

        self.install_conda_dependencies(env_name, conda_dependencies)
        self.install_pip_dependencies(env_name, pip_dependencies)

        self.log_status("Environment setup complete.")
        self.update_state({"env_setup_complete": True})

    def check_env_exists(self, env_name):
        """
        Checks if a conda environment exists.
        """
        try:
            result = subprocess.run(["conda", "env", "list", "--json"], capture_output=True, text=True, check=True)
            env_list = json.loads(result.stdout)
            for env_path in env_list["envs"]:
                if os.path.basename(env_path) == env_name:
                    return True
            return False
        except subprocess.CalledProcessError as e:
            self.log_status(f"Error checking environment existence: {e}")
            return False

    def create_env(self, env_name):
        """
        Creates a new conda environment.
        """
        self.log_status(f"Creating environment '{env_name}'...")
        try:
            subprocess.run(["conda", "create", "-n", env_name, "-y", "python=3.11"], check=True)
            self.log_status(f"Environment '{env_name}' created successfully.")
        except subprocess.CalledProcessError as e:
            self.log_status(f"Error creating environment: {e}")

    def install_conda_dependencies(self, env_name, dependencies):
        """
        Installs conda dependencies into the specified environment.
        """
        if dependencies:
            self.log_status(f"Installing conda dependencies: {dependencies}")
            try:
                subprocess.run(["conda", "install", "-n", env_name, "-y", *dependencies], check=True)
                self.log_status("Conda dependencies installed successfully.")
            except subprocess.CalledProcessError as e:
                self.log_status(f"Error installing conda dependencies: {e}")
        else:
            self.log_status("No conda dependencies to install.")

    def install_pip_dependencies(self, env_name, dependencies):
        """
        Installs pip dependencies into the specified environment.
        """
        if dependencies:
            self.log_status(f"Installing pip dependencies: {dependencies}")
            try:
                subprocess.run(["conda", "run", "-n", env_name, "pip", "install", *dependencies], check=True)
                self.log_status("Pip dependencies installed successfully.")
            except subprocess.CalledProcessError as e:
                self.log_status(f"Error installing pip dependencies: {e}")
        else:
            self.log_status("No pip dependencies to install.")

    def update_state(self, updates):
        """
        Updates the agent state and saves it to the state file.
        """
        self.state.update(updates)
        try:
            with open(self.state_path, 'w') as f:
                json.dump(self.state, f, indent=4)
            self.log_status("Agent state updated successfully.")
        except IOError as e:
            self.log_status(f"Error writing to state file: {e}")

    def log_status(self, message):
        """
        Logs a status message.  Can be extended to use a proper logging library.
        """
        print(f"[AutomatedEnvironmentSetup] {message}")

if __name__ == '__main__':
    # Example Usage (assuming env_config.json exists)
    # Create a sample env_config.json:
    # {
    #   "env_name": "my_test_env",
    #   "conda_dependencies": ["requests", "pandas"],
    #   "pip_dependencies": ["beautifulsoup4"]
    # }

    setup = AutomatedEnvironmentSetup()
    setup.process()