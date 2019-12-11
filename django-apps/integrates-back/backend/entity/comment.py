from graphene import ObjectType, String


class Comment(ObjectType):
    """ GraphQL Entity for Comments """
    id = String()  # noqa pylint: disable=invalid-name
    content = String()
    created = String()
    email = String()
    fullname = String()
    modified = String()
    parent = String()

    def resolve_id(self, info):
        """ Resolve id attribute """
        del info
        return self.id

    def resolve_content(self, info):
        """ Resolve content attribute """
        del info
        return self.content

    def resolve_created(self, info):
        """ Resolve created attribute """
        del info
        return self.created

    def resolve_email(self, info):
        """ Resolve email attribute """
        del info
        return self.email

    def resolve_fullname(self, info):
        """ Resolve fullname attribute """
        del info
        return self.fullname

    def resolve_modified(self, info):
        """ Resolve modified attribute """
        del info
        return self.modified

    def resolve_parent(self, info):
        """ Resolve parent attribute """
        del info
        return self.parent
