from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # sample known activity from initial data
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success(client):
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_duplicate_signup_rejected(client):
    activity = "Chess Club"
    email = "dup.student@mergington.edu"

    # first signup ok
    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r1.status_code == 200

    # second signup should be rejected
    r2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r2.status_code == 400


def test_unregister_success(client):
    activity = "Chess Club"
    email = "remove.me@mergington.edu"

    # signup then remove
    client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    r = client.delete(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_missing_returns_404(client):
    activity = "Chess Club"
    email = "not.signed@mergington.edu"

    r = client.delete(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r.status_code == 404
