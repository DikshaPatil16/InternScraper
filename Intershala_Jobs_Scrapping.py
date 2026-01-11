from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# Chrome setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://internshala.com/jobs/data-science-jobs/")
time.sleep(6)  # Wait for page to load

# Scroll to load more jobs
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Get all job cards
all_cards = driver.find_elements(By.CSS_SELECTOR, "div.individual_internship")
print("Total cards found:", len(all_cards))

jobs = []

for card in all_cards:
    try:
        # Only process visible cards
        if not card.is_displayed():
            continue

        # Job Role
        role_el = card.find_elements(By.CSS_SELECTOR, "a.job-title-href")
        role = role_el[0].text.strip() if role_el else "Not Found"

        # Company
        company_el = card.find_elements(By.CSS_SELECTOR, "p.company-name")
        company = company_el[0].text.strip() if company_el else "Not Found"

        # Location
        location_el = card.find_elements(By.CSS_SELECTOR, "p.row-1-item.locations a")
        if not location_el:
            location_el = card.find_elements(By.CSS_SELECTOR, "p.row-1-item.locations span")
        location = location_el[0].text.strip() if location_el else "Not Found"

        # Experience
        experience_el = card.find_elements(By.CSS_SELECTOR, "div.row-1-item span")
        experience = experience_el[0].text.strip() if experience_el else "Not Mentioned"

        # Salary
        salary_el = card.find_elements(By.CSS_SELECTOR, "span.desktop")
        salary = salary_el[0].text.strip() if salary_el else "Not Disclosed"

        # Skills
        skills_elements = card.find_elements(By.CSS_SELECTOR, "div.job_skills div.job_skill")
        skills = ", ".join([s.text for s in skills_elements]) if skills_elements else "Not Listed"

        jobs.append([role, company, skills, location, experience, salary])

    except Exception as e:
        print("Skipped a card due to error:", e)

driver.quit()

# Save to CSV
with open("Jobs_Clean.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Job_Role", "Company", "Skills", "Location", "Experience", "Salary"])
    writer.writerows(jobs)

print(f"✅ {len(jobs)} job entries saved successfully!")
