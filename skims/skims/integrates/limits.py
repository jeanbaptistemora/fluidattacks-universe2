# Units in requests-per-minute, rate limits apply to production environments

# Rate limit to all calls to Integrates
DEFAULT = 5  # at most 1 in a 3 seconds interval

# Rate limit on specific funcionalities
DO_UPDATE_EVIDENCE = 1  # at most 1 in a 1 minutes interval
