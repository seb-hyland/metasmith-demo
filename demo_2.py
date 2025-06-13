from pathlib import Path
from metasmith.python_api import *

# %%
# Import Std, define agent
dtypes, containers, transforms = Std()
path_to_agent_home = Path("demo_agent_home").resolve()
smith = Agent(
    home = Source.FromLocal(path_to_agent_home),
)


# %%
# Import the previously made data library
inputs = DataInstanceLibrary.Load(Path("all_accessions.xgdb").resolve())


# %%
# Generate workflow and run!
task = smith.GenerateWorkflow(
    given=[containers, inputs],
    transforms=[transforms],
    targets=[dtypes["hybrid_assembly"]]
)
smith.StageWorkflow(task, "clear")
smith.RunWorkflow(task)
