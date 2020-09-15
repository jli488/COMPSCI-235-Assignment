import pytest

from movie.adapters import memory_repository


MEMORY_REPO_DATA_PATH = 'datafiles/Data1000Movies.csv'


@pytest.fixture
def memory_repo():
    repo = memory_repository.MemoryRepository()
    memory_repository.populate(MEMORY_REPO_DATA_PATH, repo)
    return repo
