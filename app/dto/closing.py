""" DTO to map the Integrates fields to formstack """
import base64
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level
from ..utils import forms


def parse(request):
    """ Converts a Formstack json into Integrates format  """
    initial_dict = forms.create_dict(request)
    closing_fields = {
        "50394892": "cycle",
        "39596063": "finding",
        "47484630": "visibles",
        "39596365": "requested",
        "47700230": "verified",
        "39596368": "opened",
        "39596128": "whichOpened",
        "39596370": "closed",
        "39596202": "whichClosed"
    }
    parsed_dict = {closing_fields[k]: initial_dict[k]
                   if k in initial_dict.keys() else ""
                   for (k, v) in closing_fields.items()}
    parsed_dict["id"] = request["id"]
    parsed_dict["timestamp"] = request["timestamp"]
    if parsed_dict['visibles'] == parsed_dict['requested']:
        if parsed_dict['opened'] == '0':
            state = 'Cerrado'
        elif parsed_dict['opened'] == parsed_dict['visibles']:
            state = 'Abierto'
        else:
            state = 'Parcialmente cerrado'
    else:
        state = 'Parcialmente cerrado'
    parsed_dict['estado'] = state
    return parsed_dict


def mask_closing(closingid, mask_value):
    """Mask closing."""
    data = {
        "39596128": mask_value,
        "39596202": mask_value,
        "39596055": mask_value,
        "39597296": mask_value,
        "39596328": mask_value,
        "52862857": base64.b64encode(mask_value),
        "39596152": base64.b64encode(mask_value),
        "39596215": base64.b64encode(mask_value)
    }
    return {"data": forms.to_formstack(data), "request_id": closingid}
