# Units in requests-per-minute, rate limits apply to production environments

# Rate limit to all calls to Integrates
DEFAULT = 10  # at most 1 in a 6 seconds interval

# Rate limit on specific funcionalities
DO_UPDATE_EVIDENCE = 0.25  # at most 1 in a 4 minutes interval
