# codebuild-python-aws

A small Flask app with a fully automated CI pipeline: every push to `main` triggers **AWS CodeBuild** through a GitHub webhook, runs the **pytest** suite, and stores a ZIP artifact in **Amazon S3** only if all tests pass.


## How it works

```
git push -> GitHub -> webhook -> AWS CodeBuild -> pytest -> S3 (ZIP artifact)
                                       |
                                       +-> CloudWatch Logs
```

1. A push to `main` fires a GitHub webhook.
2. CodeBuild pulls the repo and reads `buildspec.yml`.
3. It installs Python 3.12 and dependencies, then runs `python -m pytest -v`.
4. pytest exits `0` (all passed) or `1` (any failure). A non-zero exit fails the build.
5. On success, the artifact ZIP is uploaded to S3. Logs go to CloudWatch.

## Tech stack

| Area | Tool |
|---|---|
| App | Python, Flask |
| Tests | pytest |
| Source control | GitHub (webhook trigger) |
| CI / build | AWS CodeBuild (`python-unit-test-build`) |
| Artifact storage | Amazon S3 |
| Logs | Amazon CloudWatch Logs |
| Access | IAM service role for CodeBuild |

## Project structure

Adjust to match your repo.

```
codebuild-python-demo/
├── app.py                 # Flask application
├── test_app.py            # pytest tests (functions named test_*)
├── requirements.txt
├── buildspec.yml          # CodeBuild instructions
└── README.md
```

## Run locally

```bash
pip install -r requirements.txt
python -m pytest -v
python app.py
```

pytest only discovers files named `test_*.py` / `*_test.py` and functions starting with `test_`.

## buildspec.yml

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.12
  pre_build:
    commands:
      - pip install -r requirements.txt
  build:
    commands:
      - python -m pytest -v

artifacts:
  files:
    - '**/*'
```

## AWS setup

1. **CodeBuild project:** source = this GitHub repo, runtime = Python 3.12, buildspec = `buildspec.yml`.
2. **Webhook:** enable "Rebuild every time a code change is pushed" with an event filter on `main`.
3. **Artifacts:** type = Amazon S3, pointing at your bucket, packaged as ZIP.
4. **IAM:** the CodeBuild service role needs write access to the S3 bucket and CloudWatch Logs.

## Build history (verification)

| Build | Trigger | Result | Purpose |
|---|---|---|---|
| #1 | Manual | Succeeded | Baseline |
| #2 | Manual | Failed | Intentionally broke one test (4 passed, 1 failed) to confirm pytest exit code 1 fails the build |
| #3 | Manual | Succeeded | Recovery after fixing the test |
| #4 | GitHub webhook (`GitHub-Hookshot`) | Succeeded | Confirmed push-to-build automation |

## Next steps

- Chain Source → Build → Deploy with **AWS CodePipeline**
- Deploy the artifact with **AWS CodeDeploy**
- Containerize with Docker and push to **Amazon ECR**
- Compare with **GitHub Actions** or **Jenkins** as CI engines

## Author

Dhruv Rajput · [GitHub](https://github.com/DHRUVRAJPUTTT) · [LinkedIn](https://linkedin.com/in/dhruv-rajput2007)
