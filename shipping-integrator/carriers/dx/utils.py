def handle_response(response):
    response = response.json()

    if response["Status"] == 0:
        return response
    elif response["Status"] == 4:
        response["session_expired"] = True
        return response
    else:
        status_message = response["StatusMessage"]
        raise Exception(f"Error calling DX API, {status_message}")
