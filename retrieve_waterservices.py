import requests

def extract_sites(data: str) -> str:
    """Given data, gathers the sites coming from waterservices.usgs.gov"""

    start_index = data.find("# Data for the following 1 site(s) are contained in this file") + len("# Data for the following 1 site(s) are contained in this file")
    end_index = data.find("# -----------------------------------------------------------------------------------")

    # Extract the data in between
    sites = data[start_index:end_index].strip()

    return sites

def extract_table_data(data: str) -> str:
    """Given data, gathers the table data coming from waterservices.usgs.gov"""

    # Split the response into lines and find the index where data starts
    lines = data.splitlines()
    start_index = lines.index("#     P  Provisional data subject to revision.") + 4

    # Join the lines from data_start_index to the end to form a new string
    table_data = "\n".join(lines[start_index:])

    return table_data

def get_dam_data(dam, date) -> list:
    """Gathers dam data from a dam given dam ID and the date for the data to be collected. Uses waterservices.usgs.gov"""

    # Define the URL
    url = f"https://waterservices.usgs.gov/nwis/iv/?sites={dam}&parameterCd=00065&startDT={date}T00:00:00.000-08:00&endDT={date}T23:59:59.999-08:00&siteStatus=all&format=rdb"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response text
        data = response.text

        # Split data
        site_data = extract_sites(data)
        table_data = extract_table_data(data)

        # Combine data in list
        final_data = [site_data, table_data]

        return final_data
    else:
        print("Failed to retrieve data from the URL")
        return None

if __name__ == "__main__":
    get_dam_data("", "")