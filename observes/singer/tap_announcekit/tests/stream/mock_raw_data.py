MOCK_DATE = "2000-01-1T18:18:18.123Z"
mock_post = {
    "post": {
        "id": "post654",
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
