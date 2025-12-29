# AWS Free Tier CI/CD Pipeline with Docker & GitHub Actions

## 1. Overview

This project demonstrates a simple but practical CI/CD pipeline using AWS EC2 (Free Tier), Docker, Terraform, and GitHub Actions.

A Flask web application fetches a random quote from an external API (ZenQuotes) and displays it on a web page.
Whenever code is pushed to GitHub, the application is automatically deployed to an EC2 instance via GitHub Actions.

The goal of this project is to understand **how CI/CD, Docker, and cloud infrastructure work together in a real-world flow**, rather than focusing on application complexity.

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

As a result:
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

- CI/CD pipelines focus on **repeatability and safety**, not speed
- Docker eliminates environment differences between local and production
- GitHub Actions can fully automate deployment for small-scale systems
- Infrastructure as Code (Terraform) reduces manual configuration errors

---

## 8. Future Improvements

- Use Elastic IP or Route53 for stable access
- Add health checks and rollback mechanisms
- Push Docker images to Amazon ECR
- Implement Blue/Green deployment
- Add monitoring and logging with CloudWatch