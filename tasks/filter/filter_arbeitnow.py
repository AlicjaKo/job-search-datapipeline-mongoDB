import luigi
import json
from tasks.fetch.fetch_arbeitnow import FetchArbeitnowJobsTask

class FilterArbeitnowJobsTask(luigi.Task):
    input_file = luigi.Parameter(default="data/arbeitnow_jobs.json")
    output_file = luigi.Parameter(default="data/filtered_arbeitnow_jobs.json")
    tag = luigi.Parameter(default="IT")

    def requires(self):
        return FetchArbeitnowJobsTask(output_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        with self.input().open("r") as f:
            jobs = json.load(f)

        filtered_jobs = [
            job for job in jobs if self.tag in job.get("tags", [])
        ]

        with self.output().open("w") as f:
            json.dump(filtered_jobs, f, indent=4)

        print(f"Filtered {len(filtered_jobs)} jobs with tag '{self.tag}' saved to {self.output_file}.")