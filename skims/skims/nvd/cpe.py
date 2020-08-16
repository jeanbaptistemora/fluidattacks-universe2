# Standard library
from typing import (
    Dict,
    Tuple,
)

# Local libraries
from utils.url import (
    build_query,
)


def build(
    *,
    keywords: Tuple[str, ...] = (),
    product: str,
    target_software: str = '',
    version: str,
) -> str:
    cpe_params: dict = dict(
        cpe='cpe',
        cpe_version='2.3',
        part='*',
        vendor='*',
        product=product or '__no_product__',
        version=version or '*',
        update='*',
        edition='*',
        language='*',
        software_edition='*',
        target_software=target_software or '*',
        target_hardware='*',
        other='*',
    )

    query: Dict[str, str] = dict(
        cpe_product=':'.join(cpe_params.values()).rstrip(':*'),
        form_type='Advanced',
        results_type='overview',
        search_type='all',
    )

    if keywords:
        query['query'] = ' '.join(keywords)

    return f'https://nvd.nist.gov/vuln/search/results?{build_query(query)}'
