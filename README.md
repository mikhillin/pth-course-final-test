# GCore Server Configuration Autotests

Automated UI tests for the for the [GCore server configuration page](https://gcore.com/hosting).
This project is designed as a final assignment for a PTH course.

---

## ⚙️ Used technologies

- Python 3.12
- Pytest
- Playwright (chromium only)
- Allure-pytest
- Docker & Docker Compose

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mikhillin/pth-course-final-test.git
cd pth-course-final-test
```

### 2. (Optional) Virtual environment preparation (for locally running without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```
### 3. (Optional) Run tests locally

```bash
pytest 
```
> Tests generate allure-reports automatically.
> If you don't need it, remove the '--alluredir=allure-results' flag from the pytest.ini

### 4. Run tests in Docker

```bash
docker-compose up
```
> This is installing all dependencies, running all tests and saving allure-results in the local folder

### 5. Generate Allure Report

Use locally this command:
```bash
allure serve allure-results
```
And go to the generated localhost link (e.g. http://127.0.0.1:46344)
