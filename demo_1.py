# %%
# Import dependencies
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
# Create a data library with both short and long read accessions
inputs = DataInstanceLibrary("all_accessions.xgdb")
inputs.Add(
    items = [
        (Path("inputs/accession_short").resolve(), "acc_short", "std::short_reads_accession"),
        (Path("inputs/accession_long").resolve(), "acc_long", "std::long_reads_accession"),
    ]
)
inputs.Save()

# %%
# Generate workflows for each output type and print
output_tests = [
    "long_reads_assembly",
    "short_reads_assembly",
    "hybrid_assembly",
]

print("\n\nRunning workflows...")
print("====================")
for dtype in output_tests:
    target = dtypes[dtype]
    print(f"\nRunning workflow generation for {dtype}:")

    task = smith.GenerateWorkflow(
        given=[containers, inputs],
        transforms=[transforms],
        targets=[target]
    )

    # Gather transforms and outputs
    print_outputs = [
        (step.transform.name, out.dtype_name)
        for step in task.plan.steps
        for out in step.produces
    ]

    max_transform_width = max(len(transform) for transform, _ in print_outputs)

    # Print aligned output
    for transform, output in print_outputs:
        print(f"    {transform.ljust(max_transform_width)}    ----->    {output}")
