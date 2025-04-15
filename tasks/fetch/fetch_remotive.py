import luigi
import json
from utils import fetch_with_retry

def fetch_remotive():
    url = "https://remotive.com/api/remote-jobs"

    data = fetch_with_retry(url)
    if not data:
        print("Failed to fetch data from Remotive after 3 retries.")
        return None

    print("Successfully fetched data from Remotive API.")
    return data.get("jobs", [])

class FetchRemotiveJobsTask(luigi.Task):
    output_file = luigi.Parameter(default="data/remotive_jobs.json")

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        jobs = fetch_remotive()
        if jobs is None:
            print("No data fetched. Writing an empty file to allow pipeline to continue.")
            jobs = []
        with self.output().open("w") as f:
            json.dump(jobs, f, indent=4)

        print(f"Saved {len(jobs)} jobs to {self.output_file}")