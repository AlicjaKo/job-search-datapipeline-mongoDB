import luigi
from tasks.process.run_pipeline import RunPipelineTask

if __name__ == "__main__":
    luigi.run(["RunPipelineTask"])