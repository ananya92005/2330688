import requests, json
from logger import log_info, log_debug, log_request, log_response

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJhbmFueWFzaGFybWE5ODIwMDVAZ21haWwuY29tIiwiZXhwIjoxNzgwNDgwMjI0LCJpYXQiOjE3ODA0NzkzMjQsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiJkODJlOTIwOS1lMzE5LTRmMjAtYjgzOC1iZTQ4ZDM3YThlZTkiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJhbmFueWEgc2hhcm1hIiwic3ViIjoiYWQ5Mzg2M2ItOWFiYy00NjBjLWI3NmYtYTY4NmUyODRmNGQ5In0sImVtYWlsIjoiYW5hbnlhc2hhcm1hOTgyMDA1QGdtYWlsLmNvbSIsIm5hbWUiOiJhbmFueWEgc2hhcm1hIiwicm9sbE5vIjoiMjMzMDY4OCIsImFjY2Vzc0NvZGUiOiJud3dzS3giLCJjbGllbnRJRCI6ImFkOTM4NjNiLTlhYmMtNDYwYy1iNzZmLWE2ODZlMjg0ZjRkOSIsImNsaWVudFNlY3JldCI6IndRU1hhYU1IYWN5S1RzYlcifQ.9FLOqP9G6EAhNQ2t8TO3DSqB_AvnPAFOCkh9iwKJ3Oc"

BASE_URL = "http://4.224.186.213/evaluation-service"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def fetch_depots():
    log_request("GET", f"{BASE_URL}/depots")
    r = requests.get(f"{BASE_URL}/depots", headers=HEADERS)
    log_request("GET", f"{BASE_URL}/depots", r.status_code)
    depots = r.json().get("depots", [])
    log_info(f"Fetched {len(depots)} depots")
    return depots

def fetch_tasks():
    log_request("GET", f"{BASE_URL}/vehicles")
    r = requests.get(f"{BASE_URL}/vehicles", headers=HEADERS)
    log_request("GET", f"{BASE_URL}/vehicles", r.status_code)
    data = r.json()
    # Each vehicle object IS a task directly {TaskID, Duration, Impact}
    tasks = data.get("vehicles", [])
    log_info(f"Total tasks fetched: {len(tasks)}")
    return tasks

def knapsack(tasks, capacity):
    n = len(tasks)
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    for i in range(1, n+1):
        d, imp = tasks[i-1]["Duration"], tasks[i-1]["Impact"]
        for w in range(capacity+1):
            dp[i][w] = dp[i-1][w]
            if d <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-d] + imp)
    selected, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(tasks[i-1])
            w -= tasks[i-1]["Duration"]
    return dp[n][capacity], selected

def main():
    log_info("="*50)
    log_info("Vehicle Maintenance Scheduler Started")
    log_info("="*50)
    depots = fetch_depots()
    tasks = fetch_tasks()
    results = {}
    for depot in depots:
        did, budget = depot["ID"], depot["MechanicHours"]
        impact, selected = knapsack(tasks, budget)
        log_response(did, budget, len(selected), impact)
        results[did] = {"depot_id": did, "budget": budget, "total_impact": impact,
                        "tasks_count": len(selected), "task_ids": [t["TaskID"] for t in selected]}
    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50)
    for did, r in results.items():
        print(f"Depot {did}: Budget={r['budget']}h | Impact={r['total_impact']} | Tasks={r['tasks_count']}")
    with open("output.json", "w") as f:
        json.dump(results, f, indent=2)
    log_info("Results saved to output.json")

main()