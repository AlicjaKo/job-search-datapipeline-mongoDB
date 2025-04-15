import luigi
from tasks.process.generate_report import GenerateReportTask
from tasks.load.load_database import LoadDatabaseTask

class RunPipelineTask(luigi.WrapperTask):
    def requires(self):
        return [
            GenerateReportTask(),
            LoadDatabaseTask()
        ]