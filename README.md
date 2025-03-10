# 🤖 Website Scraper

This Python script is a website scraper designed to crawl a given website and extract information such as page titles, meta titles, meta descriptions, and links. The output is saved to a CSV file.

## 📌 Features

*   **Extracts Page Metadata:**  Collects page title, meta title, and meta description from each page.
*   **Link Crawling:**  Crawls all internal links within the specified website (excluding media files).
*   **CSV Output:**  Saves the extracted data in a CSV file, with each row representing a page and columns for Page Title, Meta Title, Meta Description, and Link.  Filename format is `scrape_YYYY-MM-DD.csv`.
*   **robots.txt Respect:**  Honors the website's `robots.txt` file to avoid scraping disallowed areas.
*   **Rate Limiting:**  Includes a delay between requests to be polite to the server.
*   **Error Handling:**  Handles network errors and logs issues encountered during scraping.
*   **Logging:**  Provides a log file (`website_scraper.log`) to track the scraping process, including successes, errors, and `robots.txt` information.
*   **Development Container Ready:** Includes configuration for easy setup in development environments like GitHub Codespaces using `.devcontainer/devcontainer.json`.

## 🧩 Project Structure

```
website-scraper/
├── website_scraper.py         # Main Python script for the website scraper
├── README.md                  # Project description, setup instructions, etc.
├── requirements.txt           # Lists Python dependencies
├── .gitignore                 # Specifies intentionally untracked files that Git should ignore
├── .devcontainer/             # (Optional but Recommended) Dev Container configuration
│   └── devcontainer.json      # Configuration for development environments like GitHub Codespaces and VS Code Dev Containers
├── website_scraper.log        # (Generated after running) Log file for scraper activity and errors
└── scrape_YYYY-MM-DD.csv      # (Generated after running) CSV output file with scraped data (YYYY-MM-DD is the date of the run)
```

## 🛠️ Setup

You have several options for setting up your environment to run this website scraper:

**Option 1: Using GitHub Codespaces (Recommended - Easiest)**

1.  **Click the "Code" button** on your GitHub repository page.
2.  **Select "Create codespace on main".** This will automatically launch a fully configured development environment in your browser, including Python and all necessary dependencies.  Codespaces uses the `.devcontainer.json` file in the repository to set up the environment.
3.  **Skip to the "Configuration" and "Running the Scraper" sections.**

**Option 2: Local Setup (Without Virtual Environment)**

1.  **Clone or Download the Repository:**  Clone this repository to your local machine or download it as a ZIP file.
2.  **Install Python and pip:** Ensure you have Python 3.x and pip installed on your system.
3.  **Install Dependencies:** Navigate to the repository directory in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```
    (Alternatively, if you don't have `requirements.txt`, run: `pip install requests beautifulsoup4 lxml`)

## 🧩 Configuration

1.  **Set the Website URL:**
    *   Open the `website_scraper.py` file in a text editor.
    *   **Locate the line:** `WEBSITE_URL = "YOUR_WEBSITE_URL_HERE"`
    *   **Replace `"YOUR_WEBSITE_URL_HERE"` with the URL of the website you want to scrape.** For example: `WEBSITE_URL = "https://www.example.com"`
    *   **Save the `website_scraper.py` file.**

## 🏃🏻‍♂️ Running the Scraper

1.  **Open a terminal** (if using local setup) or use the terminal in your Codespace. Navigate to the repository directory.
2.  **Run the script:**
    ```bash
    python website_scraper.py
    ```

## 📄 Output

*   **CSV File:** After the script runs successfully, a CSV file named `scrape_YYYY-MM-DD.csv` (where `YYYY-MM-DD` is the current date) will be created in the same directory. This file contains the scraped data with columns: "Page Title", "Meta Title", "Meta Description", and "Link".
*   **Log File:** A log file named `website_scraper.log` will also be created, logging the progress and any issues during the scraping process.

## 📝 Notes

*   **robots.txt:** The scraper respects the `robots.txt` file of the target website.
*   **Rate Limiting:** A delay of 1 second is implemented between requests.
*   **Error Handling:** Basic error handling is in place.
*   **Media Files:** Links to common media files are excluded from crawling.
*   **CSV History:**  Each run creates a new dated CSV file.

## 🪪 License

This is licensed under an MIT License.