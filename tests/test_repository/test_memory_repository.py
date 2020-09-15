import pytest


def test_repository_can_add_movie(memory_repo):
    print(memory_repo.get_number_of_movies())
