# pylint: disable=too-many-lines, too-few-public-methods

import sgqlc.types
import sgqlc.types.datetime

gql_schema = sgqlc.types.Schema()


########################################################################
# Scalars and Enumerations
########################################################################
class ActionSource(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("email", "feed", "widget")


Boolean = sgqlc.types.Boolean
# In various cases the infered type Date should be DateTime
Date = sgqlc.types.datetime.DateTime


class ExternalUserSortField(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("NAME", "SEEN_AT")


Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int


class JSONObject(sgqlc.types.Scalar):
    __schema__ = gql_schema


class SegmentType(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("STRING",)


class SortOrder(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("ASC", "DESC")


String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################
class AnalyticsInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "project_id",
        "start_date",
        "end_date",
        "dimensions",
        "metrics",
        "event_type",
        "post_id",
        "widget_id",
        "feed_id",
        "client_country",
        "client_locale",
        "client_device",
        "sort_by",
        "sort_desc",
        "user_filter",
        "limit",
        "offset",
    )
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    start_date = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="start_date"
    )
    end_date = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="end_date"
    )
    dimensions = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="dimensions",
    )
    metrics = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="metrics",
    )
    event_type = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="event_type",
    )
    post_id = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="post_id"
    )
    widget_id = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Int)),
        graphql_name="widget_id",
    )
    feed_id = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="feed_id"
    )
    client_country = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="client_country",
    )
    client_locale = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="client_locale",
    )
    client_device = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="client_device",
    )
    sort_by = sgqlc.types.Field(String, graphql_name="sort_by")
    sort_desc = sgqlc.types.Field(Boolean, graphql_name="sort_desc")
    user_filter = sgqlc.types.Field(JSONObject, graphql_name="user_filter")
    limit = sgqlc.types.Field(Int, graphql_name="limit")
    offset = sgqlc.types.Field(Int, graphql_name="offset")


class LocaleEntryInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("key", "value")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")
    value = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="value"
    )


class PostContentInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("locale_id", "title", "body")
    locale_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="locale_id"
    )
    title = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="title"
    )
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="body")


########################################################################
# Output Objects and Interfaces
########################################################################
class Activity(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "type",
        "created_at",
        "project_id",
        "external_user_id",
        "external_user",
        "post_id",
        "post",
        "feedback_id",
        "feedback",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    external_user_id = sgqlc.types.Field(ID, graphql_name="external_user_id")
    external_user = sgqlc.types.Field(
        "ExternalUser", graphql_name="external_user"
    )
    post_id = sgqlc.types.Field(ID, graphql_name="post_id")
    post = sgqlc.types.Field("Post", graphql_name="post")
    feedback_id = sgqlc.types.Field(ID, graphql_name="feedback_id")
    feedback = sgqlc.types.Field("Feedback", graphql_name="feedback")


class Analytics(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "unsubs",
        "subs",
        "feedback",
        "reaction",
        "mail_sent",
        "post_views",
        "feed_views",
        "widget_imp",
        "widget_views",
    )
    unsubs = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="unsubs"
    )
    subs = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="subs")
    feedback = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="feedback"
    )
    reaction = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="reaction"
    )
    mail_sent = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="mail_sent"
    )
    post_views = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="post_views"
    )
    feed_views = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="feed_views"
    )
    widget_imp = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="widget_imp"
    )
    widget_views = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="widget_views"
    )


class AnalyticsChart(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("labels", "datasets")
    labels = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="labels",
    )
    datasets = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("ChartDataset")),
        graphql_name="datasets",
    )


class AnalyticsPost(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("posts",)
    posts = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("AnalyticsPostItem")),
        graphql_name="posts",
    )


class AnalyticsPostItem(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "title",
        "view",
        "likes",
        "dislikes",
        "neutral",
        "comment",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")
    title = sgqlc.types.Field(String, graphql_name="title")
    view = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="view")
    likes = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="likes")
    dislikes = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="dislikes"
    )
    neutral = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="neutral"
    )
    comment = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="comment"
    )


class AnalyticsReport(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "start_date",
        "end_date",
        "sort_by",
        "sort_desc",
        "headers",
        "rows",
    )
    start_date = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="start_date"
    )
    end_date = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="end_date"
    )
    sort_by = sgqlc.types.Field(String, graphql_name="sort_by")
    sort_desc = sgqlc.types.Field(Boolean, graphql_name="sort_desc")
    headers = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("AnalyticsReportHeader")),
        graphql_name="headers",
    )
    rows = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.list_of(String)), graphql_name="rows"
    )


class AnalyticsReportHeader(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("name", "type")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")


class Auditlog(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "created_at",
        "username",
        "ip_address",
        "event_type",
        "event_action",
        "metadata",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    username = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="username"
    )
    ip_address = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="ip_address"
    )
    event_type = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="event_type"
    )
    event_action = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="event_action"
    )
    metadata = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="metadata"
    )


class BeginPaddleSubscriptionResult(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("state", "metadata")
    state = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="state"
    )
    metadata = sgqlc.types.Field(JSONObject, graphql_name="metadata")


class BillingInfo(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "name",
        "email",
        "address",
        "country",
        "state",
        "card_summary",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    email = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="email"
    )
    address = sgqlc.types.Field(String, graphql_name="address")
    country = sgqlc.types.Field(String, graphql_name="country")
    state = sgqlc.types.Field(String, graphql_name="state")
    card_summary = sgqlc.types.Field(String, graphql_name="card_summary")


class ChartDataset(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("label", "data")
    label = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="label"
    )
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name="data"
    )


class EmailConfig(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "project_id",
        "send_day",
        "sending_interval",
        "filter_labels",
        "include_segmented_posts",
        "post_content_type",
        "last_send_date",
        "is_enabled",
    )
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    send_day = sgqlc.types.Field(Int, graphql_name="send_day")
    sending_interval = sgqlc.types.Field(
        String, graphql_name="sending_interval"
    )
    filter_labels = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="filter_labels"
    )
    include_segmented_posts = sgqlc.types.Field(
        Boolean, graphql_name="include_segmented_posts"
    )
    post_content_type = sgqlc.types.Field(
        String, graphql_name="post_content_type"
    )
    last_send_date = sgqlc.types.Field(Date, graphql_name="last_send_date")
    is_enabled = sgqlc.types.Field(Boolean, graphql_name="is_enabled")


class EmailDigestStatus(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "sending_interval")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    sending_interval = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="sending_interval"
    )


class ExternalUser(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "created_at",
        "seen_at",
        "name",
        "email",
        "fields",
        "is_anon",
        "is_following",
        "is_email_verified",
        "avatar",
        "is_app",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    seen_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="seen_at"
    )
    name = sgqlc.types.Field(String, graphql_name="name")
    email = sgqlc.types.Field(String, graphql_name="email")
    fields = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="fields"
    )
    is_anon = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_anon"
    )
    is_following = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_following"
    )
    is_email_verified = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_email_verified"
    )
    avatar = sgqlc.types.Field(String, graphql_name="avatar")
    is_app = sgqlc.types.Field(Boolean, graphql_name="is_app")


class FeatureField(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("value", "label")
    value = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="value"
    )
    label = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="label"
    )


class Features(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "has_custom_labels",
        "has_custom_domains",
        "has_white_label",
        "has_team",
        "has_privacy",
        "has_subscriptions",
        "has_feedback",
        "has_user_tracking",
        "has_segmentation",
        "has_custom_css",
        "has_integrations",
        "has_post_customization",
        "has_multi_language",
        "has_themes",
        "has_boosters",
        "has_email_digest",
    )
    has_custom_labels = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasCustomLabels"
    )
    has_custom_domains = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasCustomDomains"
    )
    has_white_label = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasWhiteLabel"
    )
    has_team = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasTeam"
    )
    has_privacy = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasPrivacy"
    )
    has_subscriptions = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasSubscriptions"
    )
    has_feedback = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasFeedback"
    )
    has_user_tracking = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasUserTracking"
    )
    has_segmentation = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasSegmentation"
    )
    has_custom_css = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasCustomCSS"
    )
    has_integrations = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasIntegrations"
    )
    has_post_customization = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasPostCustomization"
    )
    has_multi_language = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasMultiLanguage"
    )
    has_themes = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasThemes"
    )
    has_boosters = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasBoosters"
    )
    has_email_digest = sgqlc.types.Field(
        sgqlc.types.non_null(FeatureField), graphql_name="hasEmailDigest"
    )


class Feed(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "project",
        "name",
        "slug",
        "created_at",
        "custom_host",
        "website",
        "color",
        "url",
        "is_unindexed",
        "is_private",
        "is_readmore",
        "html_inject",
        "metadata",
        "theme",
        "version",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    project = sgqlc.types.Field(
        sgqlc.types.non_null("Project"), graphql_name="project"
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="slug")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    custom_host = sgqlc.types.Field(String, graphql_name="custom_host")
    website = sgqlc.types.Field(String, graphql_name="website")
    color = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="color"
    )
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")
    is_unindexed = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_unindexed"
    )
    is_private = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_private"
    )
    is_readmore = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_readmore"
    )
    html_inject = sgqlc.types.Field(String, graphql_name="html_inject")
    metadata = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="metadata"
    )
    theme = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="theme"
    )
    version = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="version"
    )


class Feedback(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "post_id",
        "post",
        "reaction",
        "feedback",
        "source",
        "created_at",
        "external_user_id",
        "external_user",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    post_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="post_id"
    )
    post = sgqlc.types.Field(sgqlc.types.non_null("Post"), graphql_name="post")
    reaction = sgqlc.types.Field(String, graphql_name="reaction")
    feedback = sgqlc.types.Field(String, graphql_name="feedback")
    source = sgqlc.types.Field(
        sgqlc.types.non_null(ActionSource), graphql_name="source"
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    external_user_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="external_user_id"
    )
    external_user = sgqlc.types.Field(
        sgqlc.types.non_null(ExternalUser), graphql_name="external_user"
    )


class FeedbackCount(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("reaction", "count")
    reaction = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="reaction"
    )
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")


class FeedbackToPostResult(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("user_id", "post_id", "feedback")
    user_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="user_id"
    )
    post_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="post_id"
    )
    feedback = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="feedback"
    )


class Image(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "src")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    src = sgqlc.types.Field(
        sgqlc.types.non_null(String),
        graphql_name="src",
        args=sgqlc.types.ArgDict(
            (
                (
                    "size",
                    sgqlc.types.Arg(String, graphql_name="size", default=None),
                ),
            )
        ),
    )


class Import(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "user_id",
        "status",
        "source",
        "created_at",
        "is_continuous",
        "message",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    user_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="user_id"
    )
    status = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="status"
    )
    source = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="source"
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    is_continuous = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_continuous"
    )
    message = sgqlc.types.Field(String, graphql_name="message")


class Integration(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "created_at",
        "project_id",
        "project",
        "application",
        "metadata",
        "status",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    project = sgqlc.types.Field(
        sgqlc.types.non_null("Project"), graphql_name="project"
    )
    application = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="application"
    )
    metadata = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="metadata"
    )
    status = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="status"
    )


class Invite(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "user_id",
        "project_id",
        "email",
        "created_at",
        "status",
        "member_role",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    user_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="user_id"
    )
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    email = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="email"
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    status = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="status"
    )
    member_role = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="member_role"
    )


class Invoice(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "amount", "created_at", "paid", "pdf")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    amount = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="amount"
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    paid = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="paid"
    )
    pdf = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="pdf")


class Label(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "name", "color")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    color = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="color"
    )


class Locale(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "name", "entries")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    entries = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("LocaleEntry"))
        ),
        graphql_name="entries",
    )


class LocaleEntry(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("key", "value", "base")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")
    value = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="value"
    )
    base = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="base")


class Mutation(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "save_label",
        "save_label_order",
        "delete_label",
        "save_project",
        "delete_project",
        "delete_all_posts",
        "create_demo_project",
        "save_billing_info",
        "begin_paddle_subscription",
        "ensure_paddle_subscription",
        "ensure_subscription",
        "cancel_subscription",
        "me",
        "login",
        "mail_login_link",
        "logout",
        "save_user",
        "create_user",
        "accept_invite",
        "verify_by_mail",
        "recover_by_mail",
        "resend_validation_mail",
        "create_totp_config",
        "remove_totp_config",
        "activate_totp_config",
        "add_project_member",
        "remove_project_member",
        "remove_project_invite",
        "add_project_locale",
        "remove_project_locale",
        "save_project_locale",
        "add_project_segment",
        "remove_project_segment",
        "save_post",
        "delete_post",
        "update_post_locale",
        "delete_post_locale",
        "save_feed",
        "verify_cname",
        "ensure_widget",
        "save_widget",
        "save_widget_theme",
        "delete_widget",
        "uninstall_integration",
        "update_integration",
        "import_headway",
        "import_beamer",
        "import_git_hub",
        "import_release_notes",
        "import_noticeable",
        "stop_import",
        "save_saml_config",
        "verify_saml_domain",
        "create_coupons",
        "react_to_post",
        "feedback_to_post",
        "subscribe_to_project",
        "remove_external_user",
        "send_test_email",
        "create_segment_profile",
        "remove_segment_profile",
        "send_implementation_email",
        "mark_onboarding_step_as_completed",
        "save_email_config",
        "mark_warning_as_seen",
    )
    save_label = sgqlc.types.Field(
        Label,
        graphql_name="saveLabel",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "label_id",
                    sgqlc.types.Arg(ID, graphql_name="label_id", default=None),
                ),
                (
                    "name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="name",
                        default=None,
                    ),
                ),
                (
                    "color",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="color",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_label_order = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Label))),
        graphql_name="saveLabelOrder",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "label_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(ID))
                        ),
                        graphql_name="label_ids",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_label = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="deleteLabel",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "label_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="label_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_project = sgqlc.types.Field(
        sgqlc.types.non_null("Project"),
        graphql_name="saveProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="project_id", default=None
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "website",
                    sgqlc.types.Arg(
                        String, graphql_name="website", default=None
                    ),
                ),
                (
                    "image_id",
                    sgqlc.types.Arg(ID, graphql_name="image_id", default=None),
                ),
                (
                    "favicon_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="favicon_id", default=None
                    ),
                ),
                (
                    "is_authors_listed",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_authors_listed", default=None
                    ),
                ),
                (
                    "is_whitelabel",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_whitelabel", default=None
                    ),
                ),
                (
                    "is_subscribable",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_subscribable", default=None
                    ),
                ),
                (
                    "is_slack_subscribable",
                    sgqlc.types.Arg(
                        Boolean,
                        graphql_name="is_slack_subscribable",
                        default=None,
                    ),
                ),
                (
                    "is_feedback_enabled",
                    sgqlc.types.Arg(
                        Boolean,
                        graphql_name="is_feedback_enabled",
                        default=None,
                    ),
                ),
                (
                    "ga_property",
                    sgqlc.types.Arg(
                        String, graphql_name="ga_property", default=None
                    ),
                ),
                (
                    "locale",
                    sgqlc.types.Arg(
                        String, graphql_name="locale", default=None
                    ),
                ),
            )
        ),
    )
    delete_project = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="deleteProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_all_posts = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="deleteAllPosts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    create_demo_project = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="createDemoProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_billing_info = sgqlc.types.Field(
        sgqlc.types.non_null(BillingInfo),
        graphql_name="saveBillingInfo",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "email",
                    sgqlc.types.Arg(
                        String, graphql_name="email", default=None
                    ),
                ),
                (
                    "address",
                    sgqlc.types.Arg(
                        String, graphql_name="address", default=None
                    ),
                ),
                (
                    "country",
                    sgqlc.types.Arg(
                        String, graphql_name="country", default=None
                    ),
                ),
                (
                    "state",
                    sgqlc.types.Arg(
                        String, graphql_name="state", default=None
                    ),
                ),
                (
                    "card_token",
                    sgqlc.types.Arg(
                        String, graphql_name="card_token", default=None
                    ),
                ),
                (
                    "zip_code",
                    sgqlc.types.Arg(
                        String, graphql_name="zip_code", default=None
                    ),
                ),
            )
        ),
    )
    begin_paddle_subscription = sgqlc.types.Field(
        sgqlc.types.non_null(BeginPaddleSubscriptionResult),
        graphql_name="beginPaddleSubscription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "plan_id",
                    sgqlc.types.Arg(
                        String, graphql_name="plan_id", default=None
                    ),
                ),
            )
        ),
    )
    ensure_paddle_subscription = sgqlc.types.Field(
        "Subscription",
        graphql_name="ensurePaddleSubscription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "subscription_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="subscription_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    ensure_subscription = sgqlc.types.Field(
        sgqlc.types.non_null("Subscription"),
        graphql_name="ensureSubscription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "coupon",
                    sgqlc.types.Arg(
                        String, graphql_name="coupon", default=None
                    ),
                ),
                (
                    "plan_id",
                    sgqlc.types.Arg(
                        String, graphql_name="plan_id", default=None
                    ),
                ),
            )
        ),
    )
    cancel_subscription = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="cancelSubscription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    me = sgqlc.types.Field("User", graphql_name="me")
    login = sgqlc.types.Field(
        sgqlc.types.non_null("User"),
        graphql_name="login",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="email",
                        default=None,
                    ),
                ),
                (
                    "password",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="password",
                        default=None,
                    ),
                ),
                (
                    "totp_token",
                    sgqlc.types.Arg(
                        String, graphql_name="totp_token", default=None
                    ),
                ),
                (
                    "remember",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="remember", default=None
                    ),
                ),
            )
        ),
    )
    mail_login_link = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="mailLoginLink",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="email",
                        default=None,
                    ),
                ),
            )
        ),
    )
    logout = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="logout"
    )
    save_user = sgqlc.types.Field(
        sgqlc.types.non_null("User"),
        graphql_name="saveUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        String, graphql_name="email", default=None
                    ),
                ),
                (
                    "display_name",
                    sgqlc.types.Arg(
                        String, graphql_name="display_name", default=None
                    ),
                ),
                (
                    "title",
                    sgqlc.types.Arg(
                        String, graphql_name="title", default=None
                    ),
                ),
                (
                    "password",
                    sgqlc.types.Arg(
                        String, graphql_name="password", default=None
                    ),
                ),
                (
                    "active_project_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="active_project_id", default=None
                    ),
                ),
                (
                    "image_id",
                    sgqlc.types.Arg(ID, graphql_name="image_id", default=None),
                ),
                (
                    "is_unsubs",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_unsubs", default=None
                    ),
                ),
            )
        ),
    )
    create_user = sgqlc.types.Field(
        sgqlc.types.non_null("User"),
        graphql_name="createUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        String, graphql_name="email", default=None
                    ),
                ),
                (
                    "display_name",
                    sgqlc.types.Arg(
                        String, graphql_name="display_name", default=None
                    ),
                ),
                (
                    "title",
                    sgqlc.types.Arg(
                        String, graphql_name="title", default=None
                    ),
                ),
                (
                    "password",
                    sgqlc.types.Arg(
                        String, graphql_name="password", default=None
                    ),
                ),
                (
                    "recaptcha_token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="recaptcha_token",
                        default=None,
                    ),
                ),
            )
        ),
    )
    accept_invite = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(String))
        ),
        graphql_name="acceptInvite",
        args=sgqlc.types.ArgDict(
            (
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="token",
                        default=None,
                    ),
                ),
            )
        ),
    )
    verify_by_mail = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(String))
        ),
        graphql_name="verifyByMail",
        args=sgqlc.types.ArgDict(
            (
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="token",
                        default=None,
                    ),
                ),
            )
        ),
    )
    recover_by_mail = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(String))
        ),
        graphql_name="recoverByMail",
        args=sgqlc.types.ArgDict(
            (
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="token",
                        default=None,
                    ),
                ),
            )
        ),
    )
    resend_validation_mail = sgqlc.types.Field(
        sgqlc.types.non_null("Result"), graphql_name="resendValidationMail"
    )
    create_totp_config = sgqlc.types.Field(
        sgqlc.types.non_null("TOTPConfig"), graphql_name="createTotpConfig"
    )
    remove_totp_config = sgqlc.types.Field(
        sgqlc.types.non_null("Result"), graphql_name="removeTotpConfig"
    )
    activate_totp_config = sgqlc.types.Field(
        sgqlc.types.non_null("TOTPConfig"),
        graphql_name="activateTotpConfig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="token",
                        default=None,
                    ),
                ),
            )
        ),
    )
    add_project_member = sgqlc.types.Field(
        sgqlc.types.non_null(Invite),
        graphql_name="addProjectMember",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="email",
                        default=None,
                    ),
                ),
                (
                    "member_role",
                    sgqlc.types.Arg(
                        String, graphql_name="member_role", default="owner"
                    ),
                ),
            )
        ),
    )
    remove_project_member = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="removeProjectMember",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "user_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="user_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    remove_project_invite = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="removeProjectInvite",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "invite_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="invite_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    add_project_locale = sgqlc.types.Field(
        sgqlc.types.non_null("Project"),
        graphql_name="addProjectLocale",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "locale_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="locale_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    remove_project_locale = sgqlc.types.Field(
        sgqlc.types.non_null("Project"),
        graphql_name="removeProjectLocale",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "locale_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="locale_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_project_locale = sgqlc.types.Field(
        sgqlc.types.non_null("ProjectLocale"),
        graphql_name="saveProjectLocale",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "locale_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="locale_id",
                        default=None,
                    ),
                ),
                (
                    "overrides",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(LocaleEntryInput)
                            )
                        ),
                        graphql_name="overrides",
                        default=None,
                    ),
                ),
            )
        ),
    )
    add_project_segment = sgqlc.types.Field(
        sgqlc.types.non_null("ProjectSegment"),
        graphql_name="addProjectSegment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "segment_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="segment_id",
                        default=None,
                    ),
                ),
                (
                    "type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SegmentType),
                        graphql_name="type",
                        default="STRING",
                    ),
                ),
            )
        ),
    )
    remove_project_segment = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="removeProjectSegment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "segment_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="segment_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_post = sgqlc.types.Field(
        sgqlc.types.non_null("Post"),
        graphql_name="savePost",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "contents",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(PostContentInput)
                            )
                        ),
                        graphql_name="contents",
                        default=None,
                    ),
                ),
                (
                    "user_id",
                    sgqlc.types.Arg(ID, graphql_name="user_id", default=None),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(ID, graphql_name="post_id", default=None),
                ),
                (
                    "visible_at",
                    sgqlc.types.Arg(
                        Date, graphql_name="visible_at", default=None
                    ),
                ),
                (
                    "expire_at",
                    sgqlc.types.Arg(
                        Date, graphql_name="expire_at", default=None
                    ),
                ),
                (
                    "is_draft",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_draft", default=None
                    ),
                ),
                (
                    "is_pushed",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_pushed", default=None
                    ),
                ),
                (
                    "is_pinned",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_pinned", default=None
                    ),
                ),
                (
                    "image_id",
                    sgqlc.types.Arg(ID, graphql_name="image_id", default=None),
                ),
                (
                    "external_url",
                    sgqlc.types.Arg(
                        String, graphql_name="external_url", default=None
                    ),
                ),
                (
                    "labels",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="labels",
                        default=None,
                    ),
                ),
                (
                    "segment_filters",
                    sgqlc.types.Arg(
                        JSONObject,
                        graphql_name="segment_filters",
                        default=None,
                    ),
                ),
                (
                    "flags",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(String)),
                        graphql_name="flags",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_post = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deletePost",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="post_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_post_locale = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="updatePostLocale",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="post_id",
                        default=None,
                    ),
                ),
                (
                    "locale_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="locale_id",
                        default=None,
                    ),
                ),
                (
                    "title",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="title",
                        default=None,
                    ),
                ),
                (
                    "body",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="body",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_post_locale = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deletePostLocale",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="post_id",
                        default=None,
                    ),
                ),
                (
                    "locale_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="locale_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_feed = sgqlc.types.Field(
        sgqlc.types.non_null(Feed),
        graphql_name="saveFeed",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "feed_id",
                    sgqlc.types.Arg(ID, graphql_name="feed_id", default=None),
                ),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "custom_host",
                    sgqlc.types.Arg(
                        String, graphql_name="custom_host", default=None
                    ),
                ),
                (
                    "website",
                    sgqlc.types.Arg(
                        String, graphql_name="website", default=None
                    ),
                ),
                (
                    "color",
                    sgqlc.types.Arg(
                        String, graphql_name="color", default=None
                    ),
                ),
                (
                    "is_unindexed",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_unindexed", default=None
                    ),
                ),
                (
                    "is_private",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_private", default=None
                    ),
                ),
                (
                    "is_readmore",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_readmore", default=None
                    ),
                ),
                (
                    "html_inject",
                    sgqlc.types.Arg(
                        String, graphql_name="html_inject", default=None
                    ),
                ),
                (
                    "metadata",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="metadata", default=None
                    ),
                ),
                (
                    "theme",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="theme", default=None
                    ),
                ),
                (
                    "version",
                    sgqlc.types.Arg(Int, graphql_name="version", default=None),
                ),
            )
        ),
    )
    verify_cname = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="verifyCname",
        args=sgqlc.types.ArgDict(
            (
                (
                    "feed_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="feed_id",
                        default=None,
                    ),
                ),
                (
                    "custom_host",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="custom_host",
                        default=None,
                    ),
                ),
            )
        ),
    )
    ensure_widget = sgqlc.types.Field(
        sgqlc.types.non_null("Widget"),
        graphql_name="ensureWidget",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "mode",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="mode",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_widget = sgqlc.types.Field(
        sgqlc.types.non_null("Widget"),
        graphql_name="saveWidget",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "widget_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="widget_id", default=None
                    ),
                ),
                (
                    "mode",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="mode",
                        default=None,
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(String, graphql_name="name", default=None),
                ),
                (
                    "action",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="action",
                        default=None,
                    ),
                ),
                (
                    "options",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSONObject),
                        graphql_name="options",
                        default=None,
                    ),
                ),
                (
                    "theme",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="theme", default=None
                    ),
                ),
                (
                    "version",
                    sgqlc.types.Arg(Int, graphql_name="version", default=None),
                ),
            )
        ),
    )
    save_widget_theme = sgqlc.types.Field(
        sgqlc.types.non_null("Widget"),
        graphql_name="saveWidgetTheme",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "widget_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="widget_id",
                        default=None,
                    ),
                ),
                (
                    "theme",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSONObject),
                        graphql_name="theme",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_widget = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="deleteWidget",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "widget_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="widget_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    uninstall_integration = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="uninstallIntegration",
        args=sgqlc.types.ArgDict(
            (
                (
                    "integration_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="integration_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_integration = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="updateIntegration",
        args=sgqlc.types.ArgDict(
            (
                (
                    "integration_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="integration_id",
                        default=None,
                    ),
                ),
                (
                    "options",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSONObject),
                        graphql_name="options",
                        default=None,
                    ),
                ),
            )
        ),
    )
    import_headway = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="importHeadway",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "url",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="url",
                        default=None,
                    ),
                ),
                (
                    "draft",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="draft",
                        default=None,
                    ),
                ),
            )
        ),
    )
    import_beamer = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="importBeamer",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="token",
                        default=None,
                    ),
                ),
                (
                    "draft",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="draft",
                        default=None,
                    ),
                ),
            )
        ),
    )
    import_git_hub = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="importGitHub",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "url",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="url",
                        default=None,
                    ),
                ),
                (
                    "continuous",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="continuous",
                        default=None,
                    ),
                ),
                (
                    "draft",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="draft",
                        default=None,
                    ),
                ),
            )
        ),
    )
    import_release_notes = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="importReleaseNotes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "url",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="url",
                        default=None,
                    ),
                ),
                (
                    "draft",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="draft",
                        default=None,
                    ),
                ),
            )
        ),
    )
    import_noticeable = sgqlc.types.Field(
        sgqlc.types.non_null("Result"),
        graphql_name="importNoticeable",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "url",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="url",
                        default=None,
                    ),
                ),
                (
                    "draft",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="draft",
                        default=None,
                    ),
                ),
            )
        ),
    )
    stop_import = sgqlc.types.Field(
        sgqlc.types.non_null(Import),
        graphql_name="stopImport",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "import_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="import_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_saml_config = sgqlc.types.Field(
        sgqlc.types.non_null("SAMLConfig"),
        graphql_name="saveSamlConfig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "login_url",
                    sgqlc.types.Arg(
                        String, graphql_name="login_url", default=None
                    ),
                ),
                (
                    "certificate",
                    sgqlc.types.Arg(
                        String, graphql_name="certificate", default=None
                    ),
                ),
            )
        ),
    )
    verify_saml_domain = sgqlc.types.Field(
        sgqlc.types.non_null("SAMLConfig"),
        graphql_name="verifySamlDomain",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "domain",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="domain",
                        default=None,
                    ),
                ),
            )
        ),
    )
    create_coupons = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(String))
        ),
        graphql_name="createCoupons",
        args=sgqlc.types.ArgDict(
            (
                (
                    "prefix",
                    sgqlc.types.Arg(
                        String, graphql_name="prefix", default=None
                    ),
                ),
                (
                    "plan_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="plan_id",
                        default=None,
                    ),
                ),
                (
                    "count",
                    sgqlc.types.Arg(Int, graphql_name="count", default=None),
                ),
            )
        ),
    )
    react_to_post = sgqlc.types.Field(
        sgqlc.types.non_null("ReactToPostResult"),
        graphql_name="reactToPost",
        args=sgqlc.types.ArgDict(
            (
                (
                    "user_id",
                    sgqlc.types.Arg(
                        String, graphql_name="user_id", default=None
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="post_id",
                        default=None,
                    ),
                ),
                (
                    "reaction",
                    sgqlc.types.Arg(
                        String, graphql_name="reaction", default=None
                    ),
                ),
                (
                    "fields",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="fields", default=None
                    ),
                ),
                (
                    "source",
                    sgqlc.types.Arg(
                        ActionSource, graphql_name="source", default="widget"
                    ),
                ),
            )
        ),
    )
    feedback_to_post = sgqlc.types.Field(
        sgqlc.types.non_null(FeedbackToPostResult),
        graphql_name="feedbackToPost",
        args=sgqlc.types.ArgDict(
            (
                (
                    "user_id",
                    sgqlc.types.Arg(
                        String, graphql_name="user_id", default=None
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="post_id",
                        default=None,
                    ),
                ),
                (
                    "feedback",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="feedback",
                        default=None,
                    ),
                ),
                (
                    "fields",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="fields", default=None
                    ),
                ),
                (
                    "source",
                    sgqlc.types.Arg(
                        ActionSource, graphql_name="source", default="widget"
                    ),
                ),
            )
        ),
    )
    subscribe_to_project = sgqlc.types.Field(
        sgqlc.types.non_null("SubscribeToProjectResult"),
        graphql_name="subscribeToProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "user_id",
                    sgqlc.types.Arg(
                        String, graphql_name="user_id", default=None
                    ),
                ),
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="email",
                        default=None,
                    ),
                ),
                (
                    "fields",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="fields", default=None
                    ),
                ),
                (
                    "source",
                    sgqlc.types.Arg(
                        ActionSource, graphql_name="source", default="widget"
                    ),
                ),
            )
        ),
    )
    remove_external_user = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="removeExternalUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "external_user_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="external_user_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    send_test_email = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="sendTestEmail",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(ID, graphql_name="post_id", default=None),
                ),
            )
        ),
    )
    create_segment_profile = sgqlc.types.Field(
        sgqlc.types.non_null("SegmentProfile"),
        graphql_name="createSegmentProfile",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "title",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="title",
                        default=None,
                    ),
                ),
                (
                    "rules",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSONObject),
                        graphql_name="rules",
                        default=None,
                    ),
                ),
            )
        ),
    )
    remove_segment_profile = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="removeSegmentProfile",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "title",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="title",
                        default=None,
                    ),
                ),
            )
        ),
    )
    send_implementation_email = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="sendImplementationEmail",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "inline_code",
                    sgqlc.types.Arg(
                        String, graphql_name="inline_code", default=None
                    ),
                ),
                (
                    "code",
                    sgqlc.types.Arg(String, graphql_name="code", default=None),
                ),
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="email",
                        default=None,
                    ),
                ),
            )
        ),
    )
    mark_onboarding_step_as_completed = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="markOnboardingStepAsCompleted",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "step_key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="step_key",
                        default=None,
                    ),
                ),
            )
        ),
    )
    save_email_config = sgqlc.types.Field(
        sgqlc.types.non_null(EmailConfig),
        graphql_name="saveEmailConfig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "send_day",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="send_day",
                        default=None,
                    ),
                ),
                (
                    "sending_interval",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="sending_interval",
                        default=None,
                    ),
                ),
                (
                    "filter_labels",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(String)),
                        graphql_name="filter_labels",
                        default=None,
                    ),
                ),
                (
                    "include_segmented_posts",
                    sgqlc.types.Arg(
                        Boolean,
                        graphql_name="include_segmented_posts",
                        default=None,
                    ),
                ),
                (
                    "post_content_type",
                    sgqlc.types.Arg(
                        String, graphql_name="post_content_type", default=None
                    ),
                ),
                (
                    "is_enabled",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="is_enabled", default=None
                    ),
                ),
            )
        ),
    )
    mark_warning_as_seen = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="markWarningAsSeen",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )


class Onboarding(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("progress", "items")
    progress = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="progress"
    )
    items = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("OnboardingStep")),
        graphql_name="items",
    )


class OnboardingStep(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "step_key",
        "index",
        "is_done",
        "is_active",
        "title",
        "description",
        "cta_text",
        "target_url",
    )
    step_key = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="step_key"
    )
    index = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="index")
    is_done = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_done"
    )
    is_active = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_active"
    )
    title = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="title"
    )
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )
    cta_text = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="cta_text"
    )
    target_url = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="target_url"
    )


class PageOfActivities(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("items", "page", "pages", "count")
    items = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Activity))
        ),
        graphql_name="items",
    )
    page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="page")
    pages = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="pages")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")


class PageOfAuditlog(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("items", "page", "pages", "count")
    items = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Auditlog))
        ),
        graphql_name="items",
    )
    page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="page")
    pages = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="pages")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")


class PageOfExternalUsers(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("page", "pages", "count", "items")
    page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="page")
    pages = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="pages")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")
    items = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(ExternalUser)),
        graphql_name="items",
    )


class PageOfFeedback(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("page", "pages", "count", "items")
    page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="page")
    pages = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="pages")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")
    items = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(Feedback)),
        graphql_name="items",
    )


class Plan(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "group",
        "name",
        "has_custom_labels",
        "has_custom_domains",
        "has_white_label",
        "has_team",
        "has_privacy",
        "has_subscriptions",
        "has_feedback",
        "has_user_tracking",
        "has_segmentation",
        "has_custom_css",
        "has_integrations",
        "has_post_customization",
        "has_multi_language",
        "has_themes",
        "has_boosters",
        "has_saml",
        "has_ipaccess_control",
        "has_email_digest",
        "interval",
        "price",
        "setup_price",
        "bullets",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    group = sgqlc.types.Field(String, graphql_name="group")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    has_custom_labels = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasCustomLabels"
    )
    has_custom_domains = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasCustomDomains"
    )
    has_white_label = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasWhiteLabel"
    )
    has_team = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasTeam"
    )
    has_privacy = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasPrivacy"
    )
    has_subscriptions = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasSubscriptions"
    )
    has_feedback = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasFeedback"
    )
    has_user_tracking = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasUserTracking"
    )
    has_segmentation = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasSegmentation"
    )
    has_custom_css = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasCustomCSS"
    )
    has_integrations = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasIntegrations"
    )
    has_post_customization = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasPostCustomization"
    )
    has_multi_language = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasMultiLanguage"
    )
    has_themes = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasThemes"
    )
    has_boosters = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasBoosters"
    )
    has_saml = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasSaml"
    )
    has_ipaccess_control = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasIPAccessControl"
    )
    has_email_digest = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasEmailDigest"
    )
    interval = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="interval"
    )
    price = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="price")
    setup_price = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="setup_price"
    )
    bullets = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(String))
        ),
        graphql_name="bullets",
    )


class Post(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "user_id",
        "project",
        "user",
        "created_at",
        "visible_at",
        "image_id",
        "expire_at",
        "updated_at",
        "is_draft",
        "is_pushed",
        "is_pinned",
        "is_internal",
        "external_url",
        "labels",
        "segment_filters",
        "flags",
        "default_content",
        "contents",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    user_id = sgqlc.types.Field(ID, graphql_name="user_id")
    project = sgqlc.types.Field(
        sgqlc.types.non_null("Project"), graphql_name="project"
    )
    user = sgqlc.types.Field("User", graphql_name="user")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    visible_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="visible_at"
    )
    image_id = sgqlc.types.Field(ID, graphql_name="image_id")
    expire_at = sgqlc.types.Field(Date, graphql_name="expire_at")
    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="updated_at"
    )
    is_draft = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_draft"
    )
    is_pushed = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_pushed"
    )
    is_pinned = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_pinned"
    )
    is_internal = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_internal"
    )
    external_url = sgqlc.types.Field(String, graphql_name="external_url")
    labels = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("PostLabel"))
        ),
        graphql_name="labels",
    )
    segment_filters = sgqlc.types.Field(
        JSONObject, graphql_name="segment_filters"
    )
    flags = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(String))
        ),
        graphql_name="flags",
    )
    default_content = sgqlc.types.Field(
        sgqlc.types.non_null("PostContent"), graphql_name="defaultContent"
    )
    contents = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("PostContent"))
        ),
        graphql_name="contents",
    )


class PostContent(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("post_id", "locale_id", "title", "body", "slug", "url")
    post_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="post_id"
    )
    locale_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="locale_id"
    )
    title = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="title"
    )
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="body")
    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="slug")
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class PostLabel(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("post_id", "label_id", "post", "label")
    post_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="post_id"
    )
    label_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="label_id"
    )
    post = sgqlc.types.Field(sgqlc.types.non_null(Post), graphql_name="post")
    label = sgqlc.types.Field(
        sgqlc.types.non_null(Label), graphql_name="label"
    )


class Posts(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("list", "count", "page", "pages")
    list = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Post))),
        graphql_name="list",
    )
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")
    page = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="page")
    pages = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="pages")


class Project(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "encoded_id",
        "name",
        "slug",
        "website",
        "is_authors_listed",
        "is_whitelabel",
        "is_subscribable",
        "is_slack_subscribable",
        "is_feedback_enabled",
        "is_demo",
        "is_readonly",
        "image_id",
        "favicon_id",
        "image",
        "created_at",
        "ga_property",
        "members",
        "invites",
        "labels",
        "billing_info",
        "subscription",
        "avatar",
        "favicon",
        "plan",
        "locale",
        "locales",
        "feeds",
        "integrations",
        "analytics",
        "uses_new_feed_hostname",
        "payment_gateway",
        "trial_until",
        "metadata",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    encoded_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="encodedId"
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="slug")
    website = sgqlc.types.Field(String, graphql_name="website")
    is_authors_listed = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_authors_listed"
    )
    is_whitelabel = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_whitelabel"
    )
    is_subscribable = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_subscribable"
    )
    is_slack_subscribable = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_slack_subscribable"
    )
    is_feedback_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_feedback_enabled"
    )
    is_demo = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_demo"
    )
    is_readonly = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_readonly"
    )
    image_id = sgqlc.types.Field(ID, graphql_name="image_id")
    favicon_id = sgqlc.types.Field(ID, graphql_name="favicon_id")
    image = sgqlc.types.Field(Image, graphql_name="image")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    ga_property = sgqlc.types.Field(String, graphql_name="ga_property")
    members = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("ProjectMember"))
        ),
        graphql_name="members",
    )
    invites = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Invite))
        ),
        graphql_name="invites",
    )
    labels = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Label))),
        graphql_name="labels",
    )
    billing_info = sgqlc.types.Field(BillingInfo, graphql_name="billing_info")
    subscription = sgqlc.types.Field(
        "Subscription", graphql_name="subscription"
    )
    avatar = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="avatar"
    )
    favicon = sgqlc.types.Field(String, graphql_name="favicon")
    plan = sgqlc.types.Field(sgqlc.types.non_null(Plan), graphql_name="plan")
    locale = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="locale"
    )
    locales = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("ProjectLocale"))
        ),
        graphql_name="locales",
    )
    feeds = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Feed))),
        graphql_name="feeds",
    )
    integrations = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Integration))
        ),
        graphql_name="integrations",
    )
    analytics = sgqlc.types.Field(
        Analytics,
        graphql_name="analytics",
        args=sgqlc.types.ArgDict(
            (
                (
                    "date_from",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="date_from",
                        default=None,
                    ),
                ),
                (
                    "date_to",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="date_to",
                        default=None,
                    ),
                ),
            )
        ),
    )
    uses_new_feed_hostname = sgqlc.types.Field(
        Boolean, graphql_name="usesNewFeedHostname"
    )
    payment_gateway = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="payment_gateway"
    )
    trial_until = sgqlc.types.Field(Date, graphql_name="trial_until")
    metadata = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="metadata"
    )


class ProjectLocale(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "locale_id",
        "overrides",
        "project",
        "locale",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    locale_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="locale_id"
    )
    overrides = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(LocaleEntry))
        ),
        graphql_name="overrides",
    )
    project = sgqlc.types.Field(
        sgqlc.types.non_null(Project), graphql_name="project"
    )
    locale = sgqlc.types.Field(
        sgqlc.types.non_null(Locale), graphql_name="locale"
    )


class ProjectMember(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "user_id",
        "project_id",
        "user",
        "project",
        "member_role",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    user_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="user_id"
    )
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    user = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="user")
    project = sgqlc.types.Field(
        sgqlc.types.non_null(Project), graphql_name="project"
    )
    member_role = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="member_role"
    )


class ProjectSegment(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "project_id", "type")
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    type = sgqlc.types.Field(
        sgqlc.types.non_null(SegmentType), graphql_name="type"
    )


class ProjectWarning(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "created_at", "project_id", "event_vars")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    event_vars = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="event_vars"
    )


class Query(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "me",
        "project",
        "post",
        "posts",
        "feedback_counts",
        "feedback_happiness_table",
        "feedbacks",
        "activities",
        "unread_activities",
        "check_email_digest",
        "auditlog",
        "feed",
        "feeds",
        "widget",
        "widgets",
        "import_",
        "imports",
        "labels",
        "segments",
        "segment_profiles",
        "external_users",
        "external_user_count",
        "external_user",
        "analytics",
        "analytics_chart",
        "analytics_post",
        "analyticsv2",
        "image",
        "check_subscription_plan",
        "plans",
        "invoices",
        "project_locale",
        "project_locales",
        "saml_config",
        "saml_login_url",
        "project_secret",
        "locale",
        "locales",
        "users",
        "check_active_features",
        "onboarding",
        "email_config",
        "project_warnings",
    )
    me = sgqlc.types.Field("User", graphql_name="me")
    project = sgqlc.types.Field(
        sgqlc.types.non_null(Project),
        graphql_name="project",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    post = sgqlc.types.Field(
        sgqlc.types.non_null(Post),
        graphql_name="post",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="post_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    posts = sgqlc.types.Field(
        sgqlc.types.non_null(Posts),
        graphql_name="posts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                (
                    "labels",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="labels",
                        default=None,
                    ),
                ),
                (
                    "query",
                    sgqlc.types.Arg(
                        String, graphql_name="query", default=None
                    ),
                ),
            )
        ),
    )
    feedback_counts = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(FeedbackCount))
        ),
        graphql_name="feedbackCounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(ID, graphql_name="post_id", default=None),
                ),
            )
        ),
    )
    feedback_happiness_table = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(sgqlc.types.list_of(Float))
            )
        ),
        graphql_name="feedbackHappinessTable",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(ID, graphql_name="post_id", default=None),
                ),
            )
        ),
    )
    feedbacks = sgqlc.types.Field(
        sgqlc.types.non_null(PageOfFeedback),
        graphql_name="feedbacks",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(ID, graphql_name="post_id", default=None),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
            )
        ),
    )
    activities = sgqlc.types.Field(
        sgqlc.types.non_null(PageOfActivities),
        graphql_name="activities",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "post_id",
                    sgqlc.types.Arg(ID, graphql_name="post_id", default=None),
                ),
                (
                    "external_user_id",
                    sgqlc.types.Arg(
                        ID, graphql_name="external_user_id", default=None
                    ),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                (
                    "type",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(String)),
                        graphql_name="type",
                        default=None,
                    ),
                ),
                (
                    "segment_profile",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="segmentProfile", default=None
                    ),
                ),
            )
        ),
    )
    unread_activities = sgqlc.types.Field(
        sgqlc.types.non_null("UnreadActivities"),
        graphql_name="unreadActivities",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    check_email_digest = sgqlc.types.Field(
        EmailDigestStatus,
        graphql_name="checkEmailDigest",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    auditlog = sgqlc.types.Field(
        sgqlc.types.non_null(PageOfAuditlog),
        graphql_name="auditlog",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
            )
        ),
    )
    feed = sgqlc.types.Field(
        sgqlc.types.non_null(Feed),
        graphql_name="feed",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "feed_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="feed_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    feeds = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Feed))),
        graphql_name="feeds",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    widget = sgqlc.types.Field(
        sgqlc.types.non_null("Widget"),
        graphql_name="widget",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "widget_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="widget_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    widgets = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("Widget"))
        ),
        graphql_name="widgets",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    import_ = sgqlc.types.Field(
        sgqlc.types.non_null(Import),
        graphql_name="import",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "import_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="import_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    imports = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Import))
        ),
        graphql_name="imports",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    labels = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Label))),
        graphql_name="labels",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    segments = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(String))
        ),
        graphql_name="segments",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    segment_profiles = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("SegmentProfile"))
        ),
        graphql_name="segmentProfiles",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    external_users = sgqlc.types.Field(
        sgqlc.types.non_null(PageOfExternalUsers),
        graphql_name="externalUsers",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "filters",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="filters", default=None
                    ),
                ),
                ("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),
                (
                    "sort_field",
                    sgqlc.types.Arg(
                        ExternalUserSortField,
                        graphql_name="sortField",
                        default="SEEN_AT",
                    ),
                ),
                (
                    "sort_order",
                    sgqlc.types.Arg(
                        SortOrder, graphql_name="sortOrder", default="DESC"
                    ),
                ),
            )
        ),
    )
    external_user_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="externalUserCount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "filters",
                    sgqlc.types.Arg(
                        JSONObject, graphql_name="filters", default=None
                    ),
                ),
            )
        ),
    )
    external_user = sgqlc.types.Field(
        ExternalUser,
        graphql_name="externalUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "external_user_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="external_user_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    analytics = sgqlc.types.Field(
        Analytics,
        graphql_name="analytics",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "start_date",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="startDate",
                        default=None,
                    ),
                ),
                (
                    "end_date",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="endDate",
                        default=None,
                    ),
                ),
            )
        ),
    )
    analytics_chart = sgqlc.types.Field(
        AnalyticsChart,
        graphql_name="analyticsChart",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "start_date",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="startDate",
                        default=None,
                    ),
                ),
                (
                    "end_date",
                    sgqlc.types.Arg(
                        String, graphql_name="endDate", default=None
                    ),
                ),
            )
        ),
    )
    analytics_post = sgqlc.types.Field(
        AnalyticsPost,
        graphql_name="analyticsPost",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "start_date",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="startDate",
                        default=None,
                    ),
                ),
                (
                    "end_date",
                    sgqlc.types.Arg(
                        String, graphql_name="endDate", default=None
                    ),
                ),
            )
        ),
    )
    analyticsv2 = sgqlc.types.Field(
        sgqlc.types.non_null(AnalyticsReport),
        graphql_name="analyticsv2",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AnalyticsInput),
                        graphql_name="input",
                        default=None,
                    ),
                ),
            )
        ),
    )
    image = sgqlc.types.Field(
        sgqlc.types.non_null(Image),
        graphql_name="image",
        args=sgqlc.types.ArgDict(
            (
                (
                    "image_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="image_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    check_subscription_plan = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(Plan)),
        graphql_name="checkSubscriptionPlan",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "coupon",
                    sgqlc.types.Arg(
                        String, graphql_name="coupon", default=None
                    ),
                ),
            )
        ),
    )
    plans = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Plan))),
        graphql_name="plans",
    )
    invoices = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Invoice))
        ),
        graphql_name="invoices",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    project_locale = sgqlc.types.Field(
        ProjectLocale,
        graphql_name="projectLocale",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
                (
                    "locale_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="locale_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    project_locales = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(ProjectLocale))
        ),
        graphql_name="projectLocales",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    saml_config = sgqlc.types.Field(
        sgqlc.types.non_null("SAMLConfig"),
        graphql_name="samlConfig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    saml_login_url = sgqlc.types.Field(
        String,
        graphql_name="samlLoginURL",
        args=sgqlc.types.ArgDict(
            (
                (
                    "domain",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="domain",
                        default=None,
                    ),
                ),
            )
        ),
    )
    project_secret = sgqlc.types.Field(
        sgqlc.types.non_null(String),
        graphql_name="projectSecret",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    locale = sgqlc.types.Field(
        sgqlc.types.non_null(Locale),
        graphql_name="locale",
        args=sgqlc.types.ArgDict(
            (
                (
                    "locale_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="locale_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    locales = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Locale))
        ),
        graphql_name="locales",
    )
    users = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("User"))
        ),
        graphql_name="users",
        args=sgqlc.types.ArgDict(
            (("page", sgqlc.types.Arg(Int, graphql_name="page", default=0)),)
        ),
    )
    check_active_features = sgqlc.types.Field(
        sgqlc.types.non_null(Features),
        graphql_name="checkActiveFeatures",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    onboarding = sgqlc.types.Field(
        sgqlc.types.non_null(Onboarding),
        graphql_name="onboarding",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    email_config = sgqlc.types.Field(
        sgqlc.types.non_null(EmailConfig),
        graphql_name="emailConfig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    project_warnings = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(ProjectWarning)),
        graphql_name="projectWarnings",
        args=sgqlc.types.ArgDict(
            (
                (
                    "project_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="project_id",
                        default=None,
                    ),
                ),
            )
        ),
    )


class ReactToPostResult(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("user_id", "post_id", "reaction")
    user_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="user_id"
    )
    post_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="post_id"
    )
    reaction = sgqlc.types.Field(String, graphql_name="reaction")


class Result(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("type", "message")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    message = sgqlc.types.Field(String, graphql_name="message")


class SAMLConfig(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "route",
        "login_url",
        "certificate",
        "domain",
        "is_domain_verified",
        "verify_token",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    route = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="route"
    )
    login_url = sgqlc.types.Field(String, graphql_name="login_url")
    certificate = sgqlc.types.Field(String, graphql_name="certificate")
    domain = sgqlc.types.Field(String, graphql_name="domain")
    is_domain_verified = sgqlc.types.Field(
        Boolean, graphql_name="is_domain_verified"
    )
    verify_token = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="verify_token"
    )


class SegmentProfile(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("project_id", "title", "rules")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    title = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="title"
    )
    rules = sgqlc.types.Field(JSONObject, graphql_name="rules")


class SubscribeToProjectResult(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("user_id", "email")
    user_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="user_id"
    )
    email = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="email"
    )


class Subscription(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "started_at",
        "period_started_at",
        "period_ending_at",
        "status",
        "metadata",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    started_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="started_at"
    )
    period_started_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="period_started_at"
    )
    period_ending_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="period_ending_at"
    )
    status = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="status"
    )
    metadata = sgqlc.types.Field(JSONObject, graphql_name="metadata")


class TOTPConfig(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "user_id", "qr_code", "recovery_codes")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    user_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="user_id"
    )
    qr_code = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="qr_code"
    )
    recovery_codes = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(String))
        ),
        graphql_name="recovery_codes",
    )


class UnreadActivities(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "count")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")


class User(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "hash",
        "email",
        "display_name",
        "title",
        "created_at",
        "image_id",
        "image",
        "active_project",
        "memberships",
        "avatar",
        "is_validated",
        "is_totp_enabled",
        "is_unsubs",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    hash = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="hash")
    email = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="email"
    )
    display_name = sgqlc.types.Field(String, graphql_name="display_name")
    title = sgqlc.types.Field(String, graphql_name="title")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    image_id = sgqlc.types.Field(ID, graphql_name="image_id")
    image = sgqlc.types.Field(Image, graphql_name="image")
    active_project = sgqlc.types.Field(Project, graphql_name="active_project")
    memberships = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(ProjectMember))
        ),
        graphql_name="memberships",
    )
    avatar = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="avatar"
    )
    is_validated = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_validated"
    )
    is_totp_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_totp_enabled"
    )
    is_unsubs = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="is_unsubs"
    )


class Widget(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "project_id",
        "project",
        "created_at",
        "name",
        "mode",
        "action",
        "slug",
        "options",
        "theme",
        "version",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    project_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="project_id"
    )
    project = sgqlc.types.Field(
        sgqlc.types.non_null(Project), graphql_name="project"
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(Date), graphql_name="created_at"
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    mode = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="mode")
    action = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="action"
    )
    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="slug")
    options = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="options"
    )
    theme = sgqlc.types.Field(
        sgqlc.types.non_null(JSONObject), graphql_name="theme"
    )
    version = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="version"
    )


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = Mutation
gql_schema.subscription_type = Subscription
