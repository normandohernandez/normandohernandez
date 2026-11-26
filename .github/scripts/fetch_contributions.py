"""Fetch the last year of contribution levels as [[week, weekday, level], ...]."""
import json, os, sys, urllib.request

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
QUERY = """query($login: String!) { user(login: $login) { contributionsCollection { contributionCalendar {
  weeks { contributionDays { weekday contributionLevel } } } } } }"""

login, out = sys.argv[1], sys.argv[2]
req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
    headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
)
with urllib.request.urlopen(req) as r:
    body = json.load(r)
if "errors" in body:
    sys.exit(f"GraphQL error: {body['errors']}")
weeks = body["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
grid = [[w, d["weekday"], LEVELS[d["contributionLevel"]]] for w, week in enumerate(weeks) for d in week["contributionDays"]]
json.dump(grid, open(out, "w"))
print(f"{len(grid)} days, {sum(1 for g in grid if g[2])} with contributions")
