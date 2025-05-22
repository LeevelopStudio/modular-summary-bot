# CI Summary Bot

A GitHub Actions template to post pretty CI summaries directly on Pull Requests.

## Features

- Reusable workflow
- Auto-generates Markdown summary
- Auto-posts (or updates) a PR comment
- Collapsible logs
- Duration, test stats, and artifact link support

## Setup

1. Copy this repo into your organization.
2. Call the reusable workflow using `uses:` from any CI workflow.
3. Pass test stats as inputs.

## Inputs

| Name          | Type   | Required | Description            |
|---------------|--------|----------|------------------------|
| status        | string | yes      | Job status: `success` or `failure` |
| tests_passed  | number | yes      | Number of passing tests |
| tests_failed  | number | yes      | Number of failing tests |
| coverage      | number | yes      | Code coverage (percent) |

## Example

```yaml
jobs:
  ci-summary:
    uses: your-org/ci-summary-bot/.github/workflows/reusable-ci-summary.yml@main
    with:
      status: success
      tests_passed: 100
      tests_failed: 0
      coverage: 93.1
