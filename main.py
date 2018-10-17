import argparse
import asyncio
import csv

import mygeotab


parser = argparse.ArgumentParser(description="Geotab fleet data downloader")
parser.add_argument("username", type=str, help="Your Geotab username (email address)")
parser.add_argument("password", type=str, help="Your Geotab password")
parser.add_argument("database", type=str, help="Your Geotab database name")


class Downloader:
    def __init__(self, username, password, database):
        self.client = mygeotab.API(
            username=username, password=password, database=database
        )
        self.client.authenticate()

    async def get_status_data(self):
        return await self.client.get_async("StatusData")


class CsvUtility:
    def __init__(self, data):
        clean_data = []
        for datum in data:
            datum['device'] = datum['device']['id'] 
            datum['diagnostic'] = datum['diagnostic']['id'] 
            clean_data.append(datum.values())
        
        self.data = clean_data
        self.header = list(data[0].keys())

    def write_csv(self):
        with open("data.csv", "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.header)
            writer.writerows(self.data)
            


async def main(username, password, database):
    downloader = Downloader(username, password, database)
    status_data = await downloader.get_status_data()

    csv_util = CsvUtility(status_data)
    csv_util.write_csv()

    print("Wrote data to data.csv")

if __name__ == "__main__":
    args = parser.parse_args()

    username = args.username
    password = args.password
    database = args.database

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(username, password, database))
