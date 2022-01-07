"""
Get Sessions details or create a new session based on the given course
"""
import xmlrpc.client
import sys

URL = "https://samuel-villa-open-academy-release-3908160.dev.odoo.com"
DB = "samuel-villa-open-academy-release-3908160"

def get_help():
    """
    display program usage instructions
    """
    print("""\nUsage:\n
    -h  .   .   .   .   .   .   .   .   .   .   .   .   .   .   get help
    -s <username> <password>    .   .   .   .   .   .   .   .   get session
    -c <username> <password>    .   .   .   .   .   .   .   .   get courses
    -n <username> <password> <course_id> <new_session_name> .   create new session
    """)

try:
    USERNAME = sys.argv[2]
    PASSWORD = sys.argv[3]
except:
    pass

def menu():
    """
    terminal menu 
    """
    if len(sys.argv) == 2 and sys.argv[1] == '-h':
        get_help()
    elif len(sys.argv) == 4 and sys.argv[1] == '-s':
        get_sessions()
    elif len(sys.argv) == 4 and sys.argv[1] == '-c':
        get_courses()
    elif len(sys.argv) == 6 and sys.argv[1] == '-n':
        create_session(sys.argv[4], sys.argv[5])
    else:
        get_help()

def login():
    """
    Log in and get access to DB models
    """
    USERNAME = sys.argv[2]
    PASSWORD = sys.argv[3]
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL))
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))
    return uid, models

def get_sessions():
    """
    fetch and display all sessions details 
    """
    uid, models = login()
    session_ids = models.execute_kw(DB, uid, PASSWORD, 'session.session', 'search_read', [[]], {'fields': ['name', 'number_of_seats']})
    for session in session_ids:
        print(session)

def get_courses():
    """
    fetch and display all courses details 
    """
    uid, models = login()
    course_ids = models.execute_kw(DB, uid, PASSWORD, 'course.course', 'search_read', [[]], {'fields': ['title']})
    for course in course_ids:
        print(course)

def get_course(id):
    """
    fetch course given its 'id'
    """
    uid, models = login()
    return models.execute_kw(DB, uid, PASSWORD, 'course.course', 'search_read', [[['id', '=', id]]], {'fields': ['title'], 'limit': 1})

def create_session(course_id, session_name):
    """
    create new session for the given course
    """
    uid, models = login()
    models.execute_kw(DB, uid, PASSWORD, 'session.session', 'create', [{'name': session_name, 'course': get_course(course_id)[0]['id']}])


if __name__ == "__main__":
    menu()
