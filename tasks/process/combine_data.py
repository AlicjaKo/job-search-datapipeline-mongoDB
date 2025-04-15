import luigi
import json
from tasks.filter.filter_adzuna import FilterAdzunaJobsTask
from tasks.filter.filter_remotive import FilterRemotiveJobsTask
from tasks.filter.filter_arbeitnow import FilterArbeitnowJobsTask

class CombineDataTask(luigi.Task):
    output_file = luigi.Parameter(default="data/combined_jobs.json")

    def requires(self):
        return [
            FilterAdzunaJobsTask(),
            FilterRemotiveJobsTask(),
            FilterArbeitnowJobsTask()
        ]

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        combined_data = []

        sources = [
            ("data/filtered_adzuna_jobs.json", "adzuna"),
            ("data/filtered_remotive_jobs.json", "remotive"),
            ("data/filtered_arbeitnow_jobs.json", "arbeitnow"),
        ]

        for file_path, source_name in sources:
            try:
                with open(file_path, "r") as f:
                    jobs = json.load(f)
                    for job in jobs:
                        job["source"] = source_name
                        combined_data.append(job)
            except FileNotFoundError:
                print(f"Warning: {file_path} not found. Skipping.")
            except json.JSONDecodeError:
                print(f"Warning: {file_path} contains invalid JSON. Skipping.")

        with self.output().open("w") as f:
            json.dump(combined_data, f, indent=4)

        print(f"Combined data saved to {self.output_file}.")