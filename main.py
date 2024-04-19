import requests
from datetime import datetime, timedelta
import json
import re
import csv
import sys

cookies = {
    "PHPSESSID": "8sqv0ecta3rndukt81sjpqfjqj",
    "user_session": "6712bce8e2f5c69bae1f291aa4e3c412",
    "visid_incap_2944342": "CkmCrLYxRZKQ6zA6PYV+QKnJIWYAAAAAQUIPAAAAAADaNA51BPrf6K0foC/ycu2J",
    "visid_incap_2934056": "Lv4QUR5vReSrPlrk13aT/qrJIWYAAAAAQUIPAAAAAADBLwyOnJC6HWxTblSTwjyl",
    "AMCVS_3064401053DB594D0A490D4C%40AdobeOrg": "1",
    "_ga": "GA1.1.803955706.1713490295",
    "s_v17": "DEF",
    "s_cc": "true",
    "_ga_MXXMZ1PBF7": "GS1.1.1713490294.1.1.1713490368.60.0.0",
    "visid_incap_2879622": "pbVi/2C1QSGtNHdxoXEZuN3LIWYAAAAAQUIPAAAAAADs5k31mKZ/sBkSjrcmH9cZ",
    "incap_ses_1686_2879622": "3bILH9S/LkvapuT3I+BlF9/LIWYAAAAAeExI2LhaUwlriiCS7HZIeQ==",
    "incap_ses_769_2944342": "tTqHS7fFgxvbj/+lcQmsCuvPIWYAAAAAiRdtqCnhpwq1E9PayrajUg==",
    "s_p42": "earnings%3A%20earnings-calendar",
    "s_vnum": "1714489200051%26vn%3D2",
    "s_invisit": "true; undefined_s=First%20Visit",
    "nlbi_2944342": "GsuENzr9dDbFS4sDUJ37GgAAAAAmkKI4gQJMsR+WN3Ob1YgK",
    "incap_ses_1686_2944342": "wVXGI87eSXux8Sv5I+BlF7omImYAAAAADEuTHOAkE4o5qOASn820Mw==",
    "incap_ses_1686_2934056": "Gwx2XGvWtCab9Sv5I+BlF7omImYAAAAA80cRt4eRmRPgXB8IUe3qCw==",
    "arp_scroll_position": "0",
    "s_nr": "1713514395272-Repeat",
    "s_sq": "zacksprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dearnings%25253A%252520earnings-calendar%2526link%253D26%2526region%253Dminical_place_holder%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dearnings%25253A%252520earnings-calendar%2526pidt%253D1%2526oid%253Dfunctiononclick%252528event%252529%25257BPopulateWeeklyEvents%2525281650952800%25252C%252527%252527%25252Ctrue%252529%25252CsetHighlightWeeklyPanel%252528%252529%25252CsetHighlig%2526oidt%253D2%2526ot%253DSPAN",
    "AMCV_3064401053DB594D0A490D4C%40AdobeOrg": "77933605%7CMCIDTS%7C19833%7CMCMID%7C33417854495930394175605350490587982990%7CMCAID%7CNONE%7CMCOPTOUT-1713521595s%7CNONE%7CvVersion%7C4.5"
}

headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/javascript",
    "Referer": "https://www.zacks.com/earnings/earnings-calendar",
    "Sec-Ch-Ua": "'Google Chrome';v='123', 'Not:A-Brand';v='8', 'Chromium';v='123'",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Traceparent": "00-0a3fbe16536e84e96ee0e68f1a7589a6-f2f09591e7398f51-00",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

url = "https://www.zacks.com/includes/classes/z2_class_calendarfunctions_data.php"


def getData(start, end):
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start, date_format)
    end_date = datetime.strptime(end, date_format) + timedelta(days=1)
    date = start_date

    while (True):
        req_url = f"{url}?calltype=eventscal&date={int(date.timestamp())}&type=1&search_trigger=0&0.699021724411149&_=1713490292741"
        response = requests.get(req_url, cookies=cookies, headers=headers)

        res_str = response.content.decode('utf-8')
        start_index = res_str.index('{')
        end_index = res_str.rindex('}')
        buf = response.content.decode('utf-8')[start_index: end_index + 1]
        data_dict = json.loads(buf)
        window_app_data = data_dict['data']

        for data in window_app_data:
            pattern = r'rel="([^"]+)"'
            match = re.search(pattern, data[0])
            if match:
                rel_value = match.group(1)

            append_data = {
                "Symbol": rel_value,
                "Earning Date": date.date() - timedelta(days=1),
                "Time": data[3]
            }

            csv_file_path = f'{start}__{end}.csv'
            fieldnames = ["Symbol", "Earning Date", "Time"]
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                if file.tell() == 0:
                    writer.writeheader()

                writer.writerow(append_data)

        print(date.date())
        if (date == end_date):
            break
        date = date + timedelta(days=1)


if __name__ == "__main__":
    arguments = sys.argv

    getData(arguments[1], arguments[2])