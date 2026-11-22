# Status or merge check

Identify the repository and the PR from the request, the current branch or existing evidence. Query its actual state with a connected repository tool or an authenticated CLI. Distinguish **open**, **closed without merge** and **merged**, and report the URL with its check and review state. A closed PR or a passing CI run is not proof of merge.

**Done when:** the state is reported from the remote, not inferred. If the request was only a status check, stop there: no syncing, no branch changes, no new work.
