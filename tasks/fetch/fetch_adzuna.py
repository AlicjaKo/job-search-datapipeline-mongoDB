import luigi
import json
from config import ADZUNA_API_KEY, ADZUNA_APP_ID
from utils import fetch_with_retry

def fetch_adzuna_jobs():
    base_url = "https://api.adzuna.com/v1/api/jobs/pl/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": 100,
    }
    url = f"{base_url}?app_id={params['app_id']}&app_key={params['app_key']}&results_per_page={params['results_per_page']}"

    data = fetch_with_retry(url)
    if not data:
        print("Failed to fetch data from Adzuna API after 3 retries.")
        return None

    print("Successfully fetched data from Adzuna API.")
    return data.get("results", [])

class FetchAdzunaJobsTask(luigi.Task):
    output_file = luigi.Parameter(default="data/adzuna_jobs.json")

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        jobs = fetch_adzuna_jobs()
        if jobs is None:
            print("No data fetched. Writing an empty file to allow pipeline to continue.")
            jobs = []

        with self.output().open("w") as f:
            json.dump(jobs, f, indent=4)

        print(f"Saved {len(jobs)} jobs to {self.output_file}")