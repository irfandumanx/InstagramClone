from flask import redirect, session, url_for


def loginRequirement(func):
    def check(*args, **kwargs):
        if "user" in session:
            return func(*args, **kwargs)
        return redirect(url_for("userBlueprint.getLogin"))
    check.__name__ = func.__name__
    return check
