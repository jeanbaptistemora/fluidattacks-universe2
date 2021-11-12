from datetime import (
    datetime,
)
from tap_announcekit.objs.activity import (
    Activity,
)
from tap_announcekit.objs.ext_user import (
    ExternalUser,
    ExtUserObj,
)
from tap_announcekit.objs.feed import (
    Feed,
)
from tap_announcekit.objs.id_objs import (
    ActivityId,
    ExtUserId,
    FeedbackId,
    FeedId,
    ImageId,
    IndexedObj,
    PostId,
    ProjectId,
    UserId,
    WidgetId,
)
from tap_announcekit.objs.post import (
    ActionSource,
    Feedback,
    FeedbackObj,
    Post,
)
from tap_announcekit.objs.post.content import (
    PostContent,
)
from tap_announcekit.objs.project import (
    Project,
)
from tap_announcekit.objs.widget import (
    Widget,
)

mock_datetime = datetime(2000, 1, 1)

mock_proj_id = ProjectId("proj1234")
mock_proj = Project(
    "",
    "name",
    "slug",
    None,
    True,
    True,
    True,
    False,
    False,
    True,
    True,
    None,
    None,
    mock_datetime,
    None,
    "avatar",
    "locale",
    None,
    "payment",
    None,
    "",
)
mock_proj_obj = IndexedObj(mock_proj_id, mock_proj)

mock_post_id = PostId(ProjectId("1234"), "post4321")
mock_post_obj = IndexedObj(
    mock_post_id,
    Post(
        UserId("wer"),
        mock_datetime,
        mock_datetime,
        ImageId("fsdf"),
        None,
        mock_datetime,
        True,
        False,
        False,
        True,
        None,
        None,
    ),
)

mock_post_content_obj = IndexedObj(
    mock_post_id,
    PostContent(
        "locale",
        "title1",
        "the_body",
        "slug",
        "url",
    ),
)

mock_external_user_id = ExtUserId(mock_proj_id, "extUser100")
mock_feedback_obj: FeedbackObj = IndexedObj(
    FeedbackId(mock_post_id, "feedback99"),
    Feedback(
        ":)",
        "comment",
        ActionSource.EMAIL,
        datetime(2000, 1, 1),
        mock_external_user_id,
    ),
)

mock_external_user: ExtUserObj = IndexedObj(
    mock_external_user_id,
    ExternalUser(
        mock_datetime,
        mock_datetime,
        "name",
        None,
        "",
        False,
        False,
        False,
        None,
        None,
    ),
)

mock_act_obj = IndexedObj(
    ActivityId(mock_proj_id, "act12"),
    Activity(
        "the_type",
        mock_datetime,
        mock_external_user_id,
        mock_post_id,
        mock_feedback_obj.id_obj,
    ),
)

mock_feed_obj = IndexedObj(
    FeedId(mock_proj_id, "feed1"),
    Feed(
        "name",
        "",
        mock_datetime,
        None,
        None,
        "blue",
        "url",
        False,
        False,
        False,
        None,
        "",
        "",
        2,
    ),
)

mock_widget_obj = IndexedObj(
    WidgetId(mock_proj_id, "widget1"),
    Widget(mock_datetime, "name", "", "", "", "", "", 33),
)
