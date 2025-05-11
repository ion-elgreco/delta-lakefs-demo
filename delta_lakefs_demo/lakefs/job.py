from dagster import RunConfig, job, op

from delta_lakefs_demo.lakefs.resource import LakeFSClient
from delta_lakefs_demo.utils import CodeBranch


@op(
    description="Operation to create your CodeBranch as LakeFS Branches in the provided repos scope",
    code_version="1",
)
def create_lakefs_branches(
    code_branch: CodeBranch,
    lakefs_client: LakeFSClient,
) -> None:
    """Creates lakefs branches"""
    lakefs_client.create_branch(code_branch.name)


@job(config=RunConfig(loggers={"console": {"config": {"log_level": "INFO"}}}))
def create_lakefs_branches_job() -> None:
    """Job for creating lakefsbranches which has to be executed once."""
    create_lakefs_branches()
