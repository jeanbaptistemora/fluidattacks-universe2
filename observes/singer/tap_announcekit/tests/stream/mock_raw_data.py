MOCK_DATE = "2000-01-01T18:18:18.123Z"
mock_proj = {
    "project": {
        "id": "proj12",
        "encodedId": "proj12",
        "name": "proj12",
        "slug": "",
        "website": None,
        "is_authors_listed": True,
        "is_whitelabel": True,
        "is_subscribable": True,
        "is_slack_subscribable": True,
        "is_feedback_enabled": True,
        "is_demo": True,
        "is_readonly": True,
        "image_id": "33242",
        "favicon_id": "33242",
        "created_at": MOCK_DATE,
        "ga_property": "",
        "avatar": "foo",
        "locale": "foo",
        "usesNewFeedHostname": None,
        "payment_gateway": "",
        "trial_until": None,
        "metadata": "",
    }
}
mock_post = {
    "post": {
        "project_id": "proj123",
        "user_id": None,
        "created_at": MOCK_DATE,
        "visible_at": MOCK_DATE,
        "image_id": "img1",
        "expire_at": None,
        "updated_at": MOCK_DATE,
        "is_draft": False,
        "is_pushed": False,
        "is_pinned": False,
        "is_internal": False,
        "external_url": "url",
        "segment_filters": "",
    }
}
mock_post_page = {
    "posts": {
        "list": [
            {"id": "post654", "project_id": "proj123"},
            {"id": "post655", "project_id": "proj123"},
        ],
        "count": 2,
        "page": 0,
        "pages": 1,
    }
}
mock_post_contents = {
    "post": {
        "contents": [
            {
                "post_id": "4154",
                "locale_id": "l",
                "title": "t",
                "body": "b",
                "slug": "s",
                "url": "url",
            }
        ],
    }
}
