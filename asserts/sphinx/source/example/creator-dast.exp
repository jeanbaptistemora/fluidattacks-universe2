from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.generic import FluidAsserts

with FluidAsserts(risk=MEDIUM,
                  kind=DAST,
                  message='This is a custom test!') as creator:

    creator.set_open(where='https://fluidattacks.com/integrates',
                     specific=['HTTP/Header/X-Frame-Options is missing'])

    creator.set_closed(where='https://fluidattacks.com/web',
                       specific=['HTTP/Header/X-Frame-Options is set'])
