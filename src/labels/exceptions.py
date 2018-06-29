"""Exceptions used in the labels codebase."""


class LabelsException(Exception):
    """Base exception class for this project."""


class GitHubException(LabelsException):
    """Exception for GitHub API related errors."""
