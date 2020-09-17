

# Local libraries
import sys

# Third party libraries
from click import (
    command,
    option,
)

# Local libraries
from toolbox.reports import (
    compute_bill,
    exploits,
    snapshot_bill
)


@command(name='reports', short_help="Service reports")
@option('--generate-exploits-report',
        default='')
@option('--compute-bill', 'o_compute_bill', help='Export compute bill',
        is_flag=True)
@option('--snapshot-bill', 'o_snapshot_bill', help='Print snapshot bill',
        is_flag=True)
def reports_management(
        o_generate_exploits_report,
        o_compute_bill,
        o_snapshot_bill):

    success: bool = True

    if o_generate_exploits_report:
        success = exploits.generate_exploits_report(
            o_generate_exploits_report)

    if o_compute_bill:
        success = compute_bill.create_bills()

    if o_snapshot_bill:
        success = snapshot_bill.create()

    sys.exit(0 if success else 1)
