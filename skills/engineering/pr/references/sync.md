# Sync after merge

Verify that the PR really merged, then read the project's post-merge rules. Fetch and update the intended local base safely, preserving uncommitted work and existing workspace branch names. Delete no branches, reset no unrelated changes, and start no other task or PR unless authorized. If the request was only to check status, report it without syncing.

**Done when:** the local base matches the merged remote base and every local change that existed before is still in place.
