import argparse
from datetime import datetime, timezone
import os

parser = argparse.ArgumentParser()
parser.add_argument("--status")
parser.add_argument("--job")
parser.add_argument("--workflow")
parser.add_argument("--run_id")
parser.add_argument("--actor")
parser.add_argument("--repo")
parser.add_argument("--ref")
parser.add_argument("--sha")
parser.add_argument("--tests_passed", type=int)
parser.add_argument("--tests_failed", type=int)
parser.add_argument("--coverage", type=float)
parser.add_argument("--duration", type=float)
parser.add_argument("--artifacts_url")
args = parser.parse_args()

md = f"""## {'✅' if args.status == 'success' else '❌'} CI Summary: `{args.workflow}`

- **Status**: `{args.status.upper()}`
- **Job**: `{args.job}`
- **Run ID**: [{args.run_id}](https://github.com/{args.repo}/actions/runs/{args.run_id})
- **Commit**: [`{args.sha[:7]}`](https://github.com/{args.repo}/commit/{args.sha})
- **Branch**: `{args.ref}`
- **Triggered by**: @{args.actor}
- **Duration**: `{args.duration:.2f}s`

### 🧪 Test Results
- Passed: `{args.tests_passed}`
- Failed: `{args.tests_failed}`
- Coverage: `{args.coverage:.2f}%`

"""

if args.artifacts_url:
    md += f"### 📦 Artifacts\n- [Download artifacts]({args.artifacts_url})\n\n"

for log_name in ["build.log", "test.log"]:
    if os.path.exists(log_name):
        with open(log_name) as f:
            content = f.read()[-1500] # Last ~1500 chars
        md += f"<details>\n<summary>{log_name}</summary>\n\n```bash\n{content}\n```\n</details>\n\n"

md += f"> _Generated on {datetime.now(timezone.utc).isoformat()} UTC_"

with open("ci-summary.md", "w") as f:
    f.write(md)
