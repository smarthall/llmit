from typing import Annotated
from haystack.tools import Toolset, create_tool_from_function
from git import Repo


class GitTools:
    def __init__(self, repo_path: str):
        self._repo = Repo(repo_path)
        self._toolset = Toolset([
            create_tool_from_function(self.get_commit_message),
            create_tool_from_function(self.get_commit_author),
            create_tool_from_function(self.get_revision_log_summary),
        ])

    def get_toolset(self) -> Toolset:
        return self._toolset

    def get_commit_message(
        self,
        commit_hash: Annotated[str, "The hash of the commit to get the message for"],
    ) -> str:
        """
        Use this tool to get the commit message for a given commit hash.
        """
        return self._repo.commit(commit_hash).message

    def get_commit_author(
        self,
        commit_hash: Annotated[str, "The hash of the commit to get the author for"],
    ) -> str:
        """
        Use this tool to get the author of a given commit hash.
        """
        return self._repo.commit(commit_hash).author

    def get_revision_log_summary(
        self,
        revision: Annotated[
            str, "The git revision to get the log summary for"
        ],
    ) -> str:
        """
        Use this tool to get the changed in the revision.
        """
        log = ""
        for c in self._repo.iter_commits(revision):
            log += f"{c.binsha.hex()} {c.summary}\n"

        return log
