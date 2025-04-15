import luigi
import json
from tasks.process.combine_data import CombineDataTask

class RemoveDuplicatesTask(luigi.Task):
    input_file = luigi.Parameter(default="data/combined_jobs.json")
    output_file = luigi.Parameter(default="data/cleaned_jobs.json")

    def requires(self):
        return CombineDataTask(output_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        with self.input().open("r") as f:
            combined_data = json.load(f)

        seen_ids = set()
        unique_jobs = []

        for job in combined_data:
            job_id = job.get("id")
            if job_id and job_id not in seen_ids:
                seen_ids.add(job_id)
                unique_jobs.append(job)

        with self.output().open("w") as f:
            json.dump(unique_jobs, f, indent=4)

        print(f"Removed duplicates. Cleaned data saved to {self.output_file}.")