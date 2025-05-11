from typing import Any

import dagster as dg
from dagster_delta import ClientConfig, DeltaLakePolarsIOManager, S3Config

from delta_lakefs_demo import assets
from delta_lakefs_demo.lakefs import create_lakefs_branches_job
from delta_lakefs_demo.lakefs.resource import LakeFSClient
from delta_lakefs_demo.utils import CodeBranch, get_git_branch

current_branch = get_git_branch()
lakefs_config = S3Config(
    access_key_id=dg.EnvVar("LAKEFS_ACCESS_KEY"),
    secret_access_key=dg.EnvVar("LAKEFS_SECRET_ACCESS_KEY"),
    endpoint="http://127.0.0.1:8000",
)
client_config = ClientConfig(allow_http=True)

resources: dict[str, Any] = {
    f"{layer}_delta_io_manager": DeltaLakePolarsIOManager(
        root_uri=f"lakefs://{layer}/{current_branch}",
        schema="delta_demo",
        storage_options=lakefs_config,
        client_options=client_config,
    )
    for layer in ["bronze", "silver", "gold"]
}

resources["code_branch"] = CodeBranch(name=current_branch)
resources["lakefs_client"] = LakeFSClient(
    host="http://127.0.0.1:8000",
    secret_access_key=dg.EnvVar("LAKEFS_SECRET_ACCESS_KEY"),
    access_key_id=dg.EnvVar("LAKEFS_ACCESS_KEY"),
)

all_assets = dg.load_assets_from_modules([assets], key_prefix=[current_branch])

defs = dg.Definitions(
    resources=resources, assets=all_assets, jobs=[create_lakefs_branches_job]
)
