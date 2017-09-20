from database.mongodb import student_acc, admin_acc


def get_uid_from_request(request, session):
    sid = ''

    if 'UserSession' in session:
        sid = session['UserSession']
    elif 'UserSession' in request.cookies:
        sid = request.cookies['UserSession']

    data = student_acc.find_one({'sid': sid})
    return data['uid'] if data else None


def get_admin_id_from_request(request, session):
    sid = ''

    if 'AdminSession' in session:
        sid = session['AdminSession']
    elif 'AdminSession' in request.cookies:
        sid = request.cookies['AdminSession']

    data = admin_acc.find_one({'sid': sid})
    return data['id'] if data else None
