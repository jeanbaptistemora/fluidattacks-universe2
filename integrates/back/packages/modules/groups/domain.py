# Standard libraries

# Third-party libraries
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend.dal import project as project_dal
from backend.exceptions import InvalidCommentParent
from backend.typing import Comment as CommentType
from newutils import comments as comments_utils


async def add_comment(
    info: GraphQLResolveInfo,
    project_name: str,
    email: str,
    comment_data: CommentType
) -> bool:
    """Add comment in a project."""
    parent = str(comment_data['parent'])
    content = str(comment_data['content'])
    await comments_utils.validate_handle_comment_scope(
        content,
        email,
        project_name,
        parent,
        info.context.store
    )
    if parent != '0':
        project_comments = [
            str(comment.get('user_id'))
            for comment in await project_dal.get_comments(
                project_name
            )
        ]
        if parent not in project_comments:
            raise InvalidCommentParent()
    return await project_dal.add_comment(project_name, email, comment_data)
