def message(status, msg):
    return {"status": status, "message": msg}


def validation_error(status, errors):
    return {"status": status, "errors": errors}


def err_resp(msg, code):
    return message(False, msg), code


def internal_err_resp():
    return message(False, "Something went wrong during the process!"), 500
