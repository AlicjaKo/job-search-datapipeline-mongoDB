import luigi
import json
from tasks.process.create_relevance_score import CreateRelevanceScoreTask

class GenerateReportTask(luigi.Task):
    input_file = luigi.Parameter(default="data/scored_jobs.json")
    report_file = luigi.Parameter(default="data/report.json")

    def requires(self):
        return CreateRelevanceScoreTask(output_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.report_file)

    def run(self):
        with self.input().open("r") as f:
            scored_data = json.load(f)

        sorted_jobs = sorted(scored_data, key=lambda x: x.get("relevance_score", 0), reverse=True)
        top_jobs = sorted_jobs[:10]

        report = {
            "message": "Hi, here are the top job picks for you!",
            "jobs": [
                {
                    "rank": i + 1,
                    "title": job.get("title", "N/A"),
                    "company_name": job.get("company_name", "N/A"),
                    "relevance_score": job.get("relevance_score", 0),
                    "location": job.get("candidate_required_location", "N/A"),
                    "url": job.get("url", "N/A")
                }
                for i, job in enumerate(top_jobs)
            ]
        }

        with self.output().open("w") as f:
            json.dump(report, f, indent=4)

        print(f"Generated report with {len(report['jobs'])} jobs.")