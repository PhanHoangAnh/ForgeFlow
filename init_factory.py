from agents.base_agent import BaseAgent

class Initializer(BaseAgent):
    def run(self, task_input):
        print(f"Initializing Factory State at {self.state_path}")

if __name__ == "__main__":
    init = Initializer("System_Init")
    init.run(None)