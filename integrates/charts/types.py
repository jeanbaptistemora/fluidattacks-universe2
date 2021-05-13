from typing_extensions import TypedDict


ForcesReport = TypedDict(  # pylint: disable=invalid-name
    'ForcesReport',
    {
        'fontSizeRatio': float,
        'text': str
    }
)
