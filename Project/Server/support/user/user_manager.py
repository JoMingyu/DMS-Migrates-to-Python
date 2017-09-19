from database.mongodb import student_acc, admin_acc


def get_uid_from_request(request, session):
    sid = None

    if 'UserSession' in session:
        sid = session['UserSession']
    elif 'UserSession' in request.cookies:
        sid = request.cookies['UserSession']

    return student_acc.find_one({'sid': sid})['uid']


def check_admin_from_request(request, session):
    sid = None

    if 'AdminSession' in session:
        sid = session['AdminSession']
    elif 'AdminSession' in request.cookies:
        sid = request.cookies['AdminSession']

    return True if admin_acc.find_one({'sid': sid}) else False
