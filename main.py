from scraper import Scraper
import subprocess


def main():
    scrapers = []
    all_data = []
    output_file = "data/results.csv"
    output_db = "data/duck.db"
    output_sql = "init.sql"

    for i in range(1, 13):
        url = f"https://results.eci.gov.in/ResultAcGenMay2026/statewiseS22{i}.htm"
        scraper = Scraper(url)
        scrapers.append(scraper)
        all_data.append(scraper.data)

    with open(output_file, "w") as f:
        print(",".join(all_data[0][0].keys()), file=f)

    for constituencies in all_data:
        for x in constituencies:
            raw_str = ",".join(list(x.values()))
            with open(output_file, "a") as f:
                print(raw_str, file=f)

    subprocess.run(["duckdb", output_db, "-init", output_sql], check=True)


if __name__ == "__main__":
    main()
