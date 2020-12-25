def create_DB_Template(uid):
    DB_Template = {
        'uid' : uid,
        'todolist' : [],
        'user_status' : {
            'FUNC_push' : False,
            'FUNC_delete' : False
        },
        'nickname' : 'nickname'
    }
    return DB_Template
