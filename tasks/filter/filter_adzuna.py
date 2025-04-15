import luigi
import json
from tasks.fetch.fetch_adzuna import FetchAdzunaJobsTask

class FilterAdzunaJobsTask(luigi.Task):
    input_file = luigi.Parameter(default="data/adzuna_jobs.json")
    output_file = luigi.Parameter(default="data/filtered_adzuna_jobs.json")
    category_label = luigi.Parameter(default="IT")

    def requires(self):
        return FetchAdzunaJobsTask(output_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        with self.input().open("r") as f:
            jobs = json.load(f)

        filtered_jobs = []
        for job in jobs:
            category = job.get("category", {})
            label = category.get("label", "")

            if label != self.category_label:
                continue

            if not all([
                job.get("title"),
                job.get("description"),
                job.get("location"),
                job.get("company")
            ]):
                continue

            filtered_jobs.append(job)

        with self.output().open("w") as f:
            json.dump(filtered_jobs, f, indent=4)

        print(f"Filtered {len(filtered_jobs)} IT jobs saved to {self.output_file}.")