# pylint: disable=import-error

from backend.api.resolvers import me

from ariadne import SubscriptionType

SUBSCRIPTION = SubscriptionType()

# Query resolvers
SUBSCRIPTION.set_field('counter', me.counter_resolver)
SUBSCRIPTION.set_source('counter', me.counter_generator)
