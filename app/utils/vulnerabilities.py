def format_data(vuln):
    vuln['current_state'] = vuln.get('historic_state', [{}])[-1].get('state')
    vuln['treatment'] = ('-' if vuln['current_state'] == 'closed'
                         else vuln.get('treatment', '')).lower().capitalize()

    return vuln
