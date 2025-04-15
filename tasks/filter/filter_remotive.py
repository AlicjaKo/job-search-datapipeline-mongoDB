import luigi
import json
from tasks.fetch.fetch_remotive import FetchRemotiveJobsTask

class FilterRemotiveJobsTask(luigi.Task):
    input_file = luigi.Parameter(default="data/remotive_jobs.json")
    output_file = luigi.Parameter(default="data/filtered_remotive_jobs.json")
    category = luigi.Parameter(default="Software Development")

    def requires(self):
        return FetchRemotiveJobsTask(output_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        with self.input().open("r") as f:
            jobs = json.load(f)

        filtered_jobs = [
            job for job in jobs
            if job.get("category", "").lower() == self.category.lower()
        ]

        with self.output().open("w") as f:
            json.dump(filtered_jobs, f, indent=4)

        print(f"Filtered {len(filtered_jobs)} jobs with category '{self.category}' saved to {self.output_file}.")