# 📦 Payroll Calculator

A Python-based tool that scrapes live Canadian tax data and calculates payroll deductions, including income tax, CPP, and EI for Ontario residents.

---

## 🚀 Features

* ⚙️ **Automated Tax Rate Scraping**: Scrapes federal and provincial tax brackets, CPP, and EI limits directly from official sources for the selected year
* ⚡ **High-Precision Financial Calculations**: Uses Python’s `decimal.Decimal` to ensure currency-safe arithmetic for payroll logic
* 🔁 **Persistent Yearly Rate Storage**: Saves scraped tax rates in JSON for reuse, minimizing redundant calls and enabling offline calculations

---

## 🧱 Tech Stack

| Language | Tools & Libraries                      | Infrastructure                   |
| -------- | -------------------------------------- | -------------------------------- |
| Python   | BeautifulSoup, Requests, JSON, Decimal | N/A (local script-based project) |

---

## 🔍 Project Overview

This side project was built as a hands-on exercise to explore web scraping and implement a real-world tax computation engine.
It solves the practical problem of estimating net income based on gross salary, considering all Canadian federal and Ontario provincial deductions.

* Scrapes the latest CRA tables for a given year and stores them in a structured JSON format
* Computes income tax using progressive brackets, plus CPP and EI contributions with upper limits
* Outputs a readable breakdown of gross pay, deductions, and final net pay

While not designed for public use, the project reflects experimentation with automating data ingestion, precision finance logic, and file-based I/O for reporting.

---

## 📊 Performance & Benchmarks

* 🧾 Computes payroll deductions in under **0.5 seconds**
* 💰 Accurate to **2 decimal places** using `Decimal` for currency-safe math
* 🗂 Supports **multi-year** tax rate lookups with persistent JSON caching

---

## 🧠 What I Learned

* Gained hands-on experience with **web scraping tools** like BeautifulSoup and techniques to navigate brittle or shifting web layouts
* Learned to handle **precision-sensitive financial logic** using Python’s decimal module
* Designed a basic system with **data/logic separation**, storing scraped results in JSON to support reusability and modularity
* Experienced the challenges of **real-world data extraction**, including handling malformed HTML and changes to government site structure

---

## 🏁 How to Run Locally

```bash
# clone the repo
git clone https://github.com/Dam-Sam/payroll-calculator.git

# cd into the project
cd payroll-calculator

# Run scraper (optional if rates already saved)
python rates_scraper.py

# Run payroll calculation
python payroll_calculator.py
```

> Requires Python 3 and `beautifulsoup4` and `requests`:

```bash
pip install beautifulsoup4 requests
```

---

## 🔗 Links

* [GitHub Repo](https://github.com/Dam-Sam/payroll-calculator)
