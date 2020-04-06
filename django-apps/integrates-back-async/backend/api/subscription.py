# pylint: disable=import-error

from backend.api.resolvers import subscription

from ariadne import SubscriptionType

SUBSCRIPTION = SubscriptionType()

# Query resolvers
SUBSCRIPTION.set_field('broadcast', subscription.broadcast_resolver)
SUBSCRIPTION.set_source('broadcast', subscription.broadcast_generator)
