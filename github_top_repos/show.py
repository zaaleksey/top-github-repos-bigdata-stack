from db import GitHubTopicDB


def show() -> None:
    db = GitHubTopicDB()
    top_repos = db.get_all_top()
    count = db.get_top_size()
    id, org_name, repo_name, stars_count = "id", "org_name", "repo_name", "stars_count"

    print(f"\nShow top {count} repositories:")
    print(f"{id:>15} {org_name:>30} {repo_name:>30} {stars_count:>15}")
    print("-" * 95)
    for repo in top_repos:
        print(f"{repo.id:>15} {repo.org_name:>30} {repo.repo_name:>30} {repo.stars_count:>15}")
    print(f"Count: {count}")
