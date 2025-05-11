from dagster import ConfigurableResource, InitResourceContext, get_dagster_logger
from lakefs import Repository
from lakefs.client import Client
from lakefs.exceptions import ConflictException
from pydantic import ConfigDict


class LakeFSClient(ConfigurableResource):
    """Wrapper of Lakefs Client as dagster resource, to create lakefs branches."""

    model_config = ConfigDict(extra="allow", frozen=False)
    host: str
    access_key_id: str
    secret_access_key: str
    repositories_scope: list[str] = ["bronze", "silver", "gold"]
    source_reference: str = "main"

    def setup_for_execution(  # type: ignore
        self, context: InitResourceContext | None
    ) -> "LakeFSClient":  # noqa: ARG002
        """This method is executed before the dagster pipeline runs."""
        self.client = self._create_lakefs_client()
        self.repositories = {
            repo: Repository(repo, client=self.client)
            for repo in self.repositories_scope
        }
        self._logger = get_dagster_logger()
        return self

    def _create_lakefs_client(self) -> "Client":
        """Returns a lakefs client object for interacting with a lakefs repository."""
        clt = Client(
            host=self.host,
            username=self.access_key_id,
            password=self.secret_access_key,
        )
        return clt

    def create_branch(self, branch: str) -> None:
        """Create a new branch in the specified repositories, no-op execution if already exists.

        Args:
            branch (str): The name of the branch to create.
        """

        for repo in self.repositories.values():
            try:
                repo.branch(branch).create(self.source_reference, exist_ok=False)
                self._logger.info(f"Created branch: `{branch}` in repo `{repo.id}`")
            except ConflictException:
                self._logger.info(
                    f"Branch `{branch}` already exists in repo `{repo.id}`"
                )
