# Units in requests-per-minute, rate limits apply to production environments

# Rate limit to all calls to Integrates
INTEGRATES_DEFAULT = 10  # at most 1 in a 6 seconds interval
# Rate limit on specific funcionalities
INTEGRATES_DO_UPDATE_EVIDENCE = 0.25  # at most 1 in a 4 minutes interval

# Rate limit to all calls made to non-fluid HTTP resources
LIB_HTTP_DEFAULT = 12  # at most 1 in a 5 second interval
