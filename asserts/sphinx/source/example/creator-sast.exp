from fluidasserts import SAST, HIGH
from fluidasserts.utils.generic import FluidAsserts

with FluidAsserts(risk=HIGH,
                  kind=SAST,
                  message='This is a custom test!') as creator:

    # lines 4 and 8 are vulnerable
    creator.set_open(where='Repo/Folder/File.py',
                     specific=[4, 8])

    # lines 7 and 23 are ok
    creator.set_closed(where='Repo/Folder/File.py',
                       specific=[7, 23])
