from pathlib import Path
from metasmith.python_api import *

# %%
# The Std() endpoint exposes the Metasmith "standard library"
dtypes, containers, transforms = Std()


# %%
# Create a local agent instance
path_to_agent_home = Path("demo_agent_home").resolve()
smith = Agent(
    home = Source.FromLocal(path_to_agent_home),
)
smith.Deploy()


# %%
# Create a library which contains our input data
accession_short = DataInstanceLibrary("accession_short.xgdb")
accession_short.Add(
    items = [
        (Path("inputs/accession_short").resolve(), "short_acc", "std::short_reads_accession")
    ]
)


# %%
# Generate and run a workflow to transform our SRA accession into read stats
task = smith.GenerateWorkflow(
    given      = [containers, accession_short],
    transforms = [transforms],
    targets    = [dtypes["read_stats"]]
)
smith.StageWorkflow(task, "clear")
smith.RunWorkflow(task)


# %%
# Do it again for long reads
accession_long = DataInstanceLibrary("accession_long.xgdb")
accession_long.Add(
    items = [
        (Path("inputs/accession_long").resolve(), "accession", "std::long_reads_accession")
    ]
)
task = smith.GenerateWorkflow(
    given      = [containers, accession_long],
    transforms = [transforms],
    targets    = [dtypes["read_stats"]]
)
smith.StageWorkflow(task, "clear")
smith.RunWorkflow(task)


# %%
# Can be called to check the status of a task
smith.CheckWorkflow(task)


# %%
# Transferring results to a specific output location is supported
results_source = smith.GetResultSource(task, check_exists=True)
output_dir = Path("output_transfer/").resolve()
destination = Source.FromLocal(output_dir)
mover = Logistics()
mover.QueueTransfer(results_source, destination)
mover.ExecuteTransfers()
