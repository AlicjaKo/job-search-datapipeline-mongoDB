import luigi
import json
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, JOBS_COLLECTION
from tasks.process.create_relevance_score import CreateRelevanceScoreTask

class LoadDatabaseTask(luigi.Task):
    input_file = luigi.Parameter(default="data/scored_jobs.json")

    def requires(self):
        return CreateRelevanceScoreTask(output_file=self.input_file)

    def output(self):
        return luigi.LocalTarget("data/db_load_success.txt")

    def run(self):
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[JOBS_COLLECTION]

        try:
            with open(self.input_file, "r") as f:
                jobs = json.load(f)

            if jobs:
                collection.insert_many(jobs)
                print(f"Successfully inserted {len(jobs)} job postings into the '{JOBS_COLLECTION}' collection.")
            else:
                print("No jobs found in the JSON file to insert.")

            with self.output().open("w") as f:
                f.write("Database load successful.")

        except Exception as e:
            print(f"Failed to load jobs into MongoDB: {e}")

        finally:
            client.close()