# AWS Free Tier CI/CD Pipeline with Docker & GitHub Actions

## 1. Overview

This project demonstrates a simple but practical CI/CD pipeline using AWS EC2 (Free Tier), Docker, Terraform, and GitHub Actions.

The main goal of this project is to understand and explain the end-to-end deployment flow**, including:
- how GitHub Actions triggers deployments
- how Docker images are built, replaced, and cleaned up
- how health checks and remote commands are executed safely

Rather than focusing on application complexity, this project focuses on operational reliability and deployment automation**, which are essential skills for DevOps / Cloud Engineers.

---

## 2. Architecture

Developer
|
| git push
v
GitHub Repository
|
| GitHub Actions (CI/CD)
v
EC2 (Ubuntu)
|
| Docker build & run
v
Flask Application (Port 80)

### Components

- **GitHub Actions**
  - Runs CI (test) and CD (deployment) pipelines
- **EC2 (Ubuntu)**
  - Hosts Docker and runs the application container
- **Docker**
  - Packages the Flask application into a portable container
- **Terraform**
  - Used to provision AWS infrastructure (EC2, security groups)
- **ZenQuotes API**
  - External API used to fetch a random quote

Additional operational components:

- **AWS Systems Manager (SSM)**
  - Used to execute remote Docker commands without direct SSH login
- **Python automation scripts**
  - Perform health checks before deployment
  - Trigger SSM `send_command` only when the service is healthy

---

## 3. Application Behavior

- The Flask app exposes a single endpoint: `/`
- On each request:
  1. The app calls `https://zenquotes.io/api/random`
  2. Extracts the quote and author from the response
  3. Renders them as a simple HTML page

If the API request fails, a fallback message is displayed instead.

This design intentionally keeps the app simple so the focus remains on **deployment and automation**, not business logic.

---

## 4. CI/CD Flow（Most Important Section）

### CI (Continuous Integration)

Triggered on:
- `push` to the `main` branch
- `pull_request`

Steps:
1. Checkout source code
2. Set up Python
3. Install dependencies
4. Run pytest

This ensures that broken code is never deployed.

---

### CD (Continuous Deployment)

Triggered on:
- `push` to `main`

Steps:
1. GitHub Actions connects to EC2 via SSH
2. Pulls the latest code from GitHub
3. Builds a new Docker image on EC2
4. Stops and removes the existing container (if any)
5. Runs a new container with the updated image

---

## Deployment Safety Mechanisms

To prevent broken deployments and unnecessary downtime, the following safeguards are implemented:

### Health Check Before Deployment
- A Python script (`health_check.py`) checks the running application via HTTP
- Deployment proceeds only if HTTP 200 is returned
- This prevents replacing a healthy service with a broken one

### Remote Command Execution via SSM
- Docker commands are executed using AWS Systems Manager
- No direct SSH login is required for deployment
- This improves security and auditability

### Docker Image Cleanup
- Old and unused Docker images are removed after deployment
- Prevents disk space exhaustion on Free Tier EC2 instances


As a result of these deployment safeguards:
- **No manual SSH or deployment steps are required**
- The running application is always in sync with the GitHub repository

---

## 5. How to Run Manually (For Verification)

On EC2 (Ubuntu):

```bash
git clone git@github.com:<your-repo>/aws-free-tier-cicd-pipeline.git
cd aws-free-tier-cicd-pipeline
docker build -t myapp:latest ./app
docker run -d -p 80:5000 --name myapp myapp:latest

Access the app via:
http://<EC2_PUBLIC_IP>/
```

---

## 6. Security & Cost Considerations

- SSH access is restricted via Security Group rules
- GitHub Secrets are used to store:
  - EC2 public IP
  - SSH username
  - Private key
- Elastic IP is intentionally not used to avoid unnecessary cost
- EC2 instances are stopped when not in use to stay within Free Tier limits

---

## 7. Lessons Learned

- CI/CD is not only about automation, but about reducing risk
- Health checks are essential before replacing running services
- Docker image cleanup is necessary on long-running EC2 instances
- SSM provides a safer alternative to SSH-based deployments

---

## 8. Future Improvements

- Use Elastic IP or Route53 for stable access
- Add health checks and rollback mechanisms
- Push Docker images to Amazon ECR
- Implement Blue/Green deployment
- Add monitoring and logging with CloudWatch