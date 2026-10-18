import urllib.request
import http.cookiejar
import json

# 1. Health check
res_h = urllib.request.urlopen("http://127.0.0.1:8000/health")
health_data = json.loads(res_h.read().decode("utf-8"))
print("Health check response:", health_data)

# 2. Client A connects
jar_a = http.cookiejar.CookieJar()
opener_a = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar_a))
res_a = opener_a.open("http://127.0.0.1:8000/api/state")
data_a = json.loads(res_a.read().decode("utf-8"))
sid_a = data_a.get("session_id")
print("Client A Session ID:", sid_a)

# Client A selects rooster 2
req_a = urllib.request.Request(
    "http://127.0.0.1:8000/api/select-rooster",
    data=json.dumps({"rooster_index": 2, "ai_difficulty": "veteran", "series_mode": "bo5"}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
post_res_a = json.loads(opener_a.open(req_a).read().decode("utf-8"))
print("Client A Stage:", post_res_a.get("stage"), "| Rooster:", post_res_a.get("human_rooster", {}).get("rooster_name"))

# 3. Client B connects (distinct cookie jar)
jar_b = http.cookiejar.CookieJar()
opener_b = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar_b))
res_b = opener_b.open("http://127.0.0.1:8000/api/state")
data_b = json.loads(res_b.read().decode("utf-8"))
sid_b = data_b.get("session_id")
print("Client B Session ID:", sid_b)
print("Client B Stage:", data_b.get("stage"), "| Rooster:", data_b.get("human_rooster"))

# 4. Assertions
assert sid_a != sid_b, "Client A and Client B must have distinct session IDs!"
assert post_res_a.get("stage") == 2, "Client A should have advanced to Stage 2"
assert data_b.get("stage") == 1, "Client B should remain in fresh Stage 1"
assert data_b.get("human_rooster") is None, "Client B must NOT see Client A's selected rooster"

print(">>> SUCCESS: Multi-tenant session isolation verified 100% working! <<<")
