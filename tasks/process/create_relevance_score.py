import luigi
import json
from tasks.process.check_for_duplicates import RemoveDuplicatesTask

class CreateRelevanceScoreTask(luigi.Task):
    input_file = luigi.Parameter(default="data/cleaned_jobs.json")
    output_file = luigi.Parameter(default="data/scored_jobs.json")

    def requires(self):
        return RemoveDuplicatesTask()

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        with self.input().open("r") as f:
            cleaned_data = json.load(f)

        KEYWORD_WEIGHTS = {
            "remote": 2,
            "java": 5,
            "cloud": 4,
            "python": 3,
            "kubernetes": 3,
            "AI/ML": 6,
            "full_time": 2,
            "part_time": 1,
            "contract": 1,
            "docker": 3,
            "security": 4,
        }

        for job in cleaned_data:
            score = 0

            description = job.get("description", "").lower()
            for keyword, weight in KEYWORD_WEIGHTS.items():
                if keyword in description:
                    score += weight

            tags = job.get("tags", [])
            for tag in tags:
                if tag.lower() in KEYWORD_WEIGHTS:
                    score += KEYWORD_WEIGHTS[tag.lower()]

            job_type = job.get("job_type", "").lower()
            if job_type in KEYWORD_WEIGHTS:
                score += KEYWORD_WEIGHTS[job_type]

            job["relevance_score"] = score

        with self.output().open("w") as f:
            json.dump(cleaned_data, f, indent=4)

        print(f"Relevance scores calculated and saved to {self.output_file}.")