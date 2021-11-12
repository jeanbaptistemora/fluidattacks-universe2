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

_mock_feedback = {
    "id": "feedback42",
    "post_id": "post44",
    "reaction": None,
    "feedback": "comment",
    "source": "widget",
    "created_at": MOCK_DATE,
    "external_user_id": "extUser23",
}
mock_feedbacks = {
    "feedbacks": {
        "page": 0,
        "pages": 1,
        "count": 1,
        "items": [_mock_feedback, _mock_feedback],
    }
}

mock_ext_users_ids = {
    "externalUsers": {
        "page": 0,
        "pages": 1,
        "count": 1,
        "items": [
            {"id": "extUser99"},
            {"id": "extUser100"},
        ],
    }
}
mock_ext_user = {
    "externalUser": {
        "created_at": MOCK_DATE,
        "seen_at": MOCK_DATE,
        "name": "extUser99",
        "email": None,
        "fields": "",
        "is_anon": False,
        "is_following": False,
        "is_email_verified": False,
        "avatar": None,
        "is_app": False,
    }
}

_mock_activity = {
    "id": "act6",
    "type": "act_type",
    "created_at": MOCK_DATE,
    "project_id": "proj1",
    "external_user_id": "user",
    "post_id": "post1",
    "feedback_id": "feedbk1",
}
mock_activities = {
    "activities": {
        "page": 0,
        "pages": 1,
        "count": 1,
        "items": [_mock_activity],
    }
}

mock_feed_ids = {
    "feeds": [
        {"id": "feed1"},
        {"id": "feed2"},
    ]
}
mock_feed = {
    "feed": {
        "name": "name",
        "slug": "slug",
        "created_at": MOCK_DATE,
        "custom_host": None,
        "website": None,
        "color": "color",
        "url": "url",
        "is_unindexed": True,
        "is_private": True,
        "is_readmore": True,
        "html_inject": None,
        "metadata": "",
        "theme": "",
        "version": 2,
    }
}

mock_widgets_ids = {
    "widgets": [
        {"id": "widget1"},
        {"id": "widget2"},
    ]
}
mock_widget = {
    "widget": {
        "created_at": MOCK_DATE,
        "name": "name",
        "mode": "mode",
        "action": "action",
        "slug": "slug",
        "options": "",
        "theme": "",
        "version": 63,
    }
}
