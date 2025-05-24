from v0.errors.app_error import App_Error


class CreateAnalyticMetadata:
    repo = None

    def __init__(self, analytic_repo) -> None:
        self.repo = analytic_repo

    def validate(self, data):
        if "user_id" not in data:
            raise App_Error(
                "CREATE-ANALYTIC-METADA-ERROR: id is required", 400)
        if "metadata" not in data:
            raise App_Error(
                "CREATE-ANALYTIC-METADA-ERROR: metadata is required", 400)

    def execute(self, data):
        self.repo.create_analytics(data)
        return
