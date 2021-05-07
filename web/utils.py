def message(status, msg):
    response_object = {"status": status, "message": msg}
    return response_object


def validation_error(status, errors):
    response_object = {"status": status, "errors": errors}

    return response_object


def err_resp(msg, code):
    err = message(False, msg)
    return err, code


def internal_err_resp():
    err = message(False, "Something went wrong during the process!")
    return err, 500
