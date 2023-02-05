# Summarize wrapper - no guaranteed results!

import requests
import sys
import html

def get_summary_and_takeaways(url: str) -> tuple:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
    post_response = requests.post("https://labs.kagi.com/v1/summarization", json={"url": url}, headers=headers)
    post_data = post_response.json()

    for i in range(3):
        response = requests.get(f"https://labs.kagi.com/v1/summary_status?url={url}", headers=headers)
        data = response.json()
        if 'summary' in data:
            takeaways_response = requests.post(f"https://labs.kagi.com/v1/takeaways", json={"url": url}, headers=headers)
            takeaways_data = takeaways_response.json()
            if 'takeaways' in takeaways_data:
                try:
                    return (html.unescape(data['summary']), html.unescape(takeaways_data['takeaways']).replace("<br><br>", "\n- "))
                except TypeError as e:
                    continue
            else:
                continue
        else:
            continue
    return None

if len(sys.argv) == 1:
    print("Please provide the URL as an argument")
    sys.exit(1)

url = sys.argv[1]
result = get_summary_and_takeaways(url)

if result is None:
    print("None")
else:
    if type(result) is tuple:
        print('\033[1m'+"\nSummary:"+'\033[0m')
        print(result[0])
        print('\033[1m'+"\nTakeaways:"+'\033[0m')
        print("\n".join(f"- {t}" for t in result[1].split("\n")))
    else:
        print('\033[1m'+"\nSummary:"+'\033[0m')
        print(result)
