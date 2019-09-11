from fluidasserts import DAST, LOW
from fluidasserts.utils.generic import FluidAsserts

with FluidAsserts(risk=LOW,
                  kind=DAST,
                  message='This will fail :( but gracefully :)') as creator:

    raise Exception('There is no Internet Connection!')
