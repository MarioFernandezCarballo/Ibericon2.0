from utils.auth import userSignup, userLogin, getUserOnly, resetUserInfo


def userSignupApi(database, form):
    _, apiResult = userSignup({"email": form.email, "password": form.password})
    return apiResult


def userLoginApi(form):
    _, apiResult = userLogin({"email": form.mail, "password": form.password})
    return apiResult


def getUserOnlyApi(pl):
    return getUserOnly(pl)


def resetUserInfoApi():
    _, apiResult = resetUserInfo()
    return apiResult
