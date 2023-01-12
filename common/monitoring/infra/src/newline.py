import base64


def lambda_handler(event, context):  # NOSONAR
    output = []

    for record in event["records"]:
        payload = base64.b64decode(record["data"]).decode("utf-8")
        row_w_newline = payload + "\n"
        row_w_newline = base64.b64encode(row_w_newline.encode("utf-8"))

        output_record = {
            "data": row_w_newline,
            "recordId": record["recordId"],
            "result": "Ok",
        }
        output.append(output_record)

    return {"records": output}
