set shell := ["bash", "-uc"]

_default:
    just --list

venv:
	uv sync

create-lakefs-branch:
	uv run dagster job execute -f delta_lakefs_demo/repo.py --job create_lakefs_branches_job

# Workflow to run dagster locally
dagster-dev:
    just create-lakefs-branch
    uv run dagster dev

# Workflow to deploy to kubernetes
# deploy:
# 	just create-lakefs-branch
# 	uv run dagster-uc deployment deploy

# Remove environment and caches
[confirm("Are you sure you want to delete everything?")]
clean:
	@rm -rf .venv/
	@rm -rf .pytest_cache/
	@rm -rf .ruff_cache/
