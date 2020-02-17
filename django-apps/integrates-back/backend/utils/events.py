def format_data(event):
    historic_state = event.get('historic_state', [{}, {}])
    event['closing_date'] = '-'
    if historic_state[-1].get('state') == 'SOLVED':
        event['closing_date'] = historic_state[-2].get('date', '')

    return event
