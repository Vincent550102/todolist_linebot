def create_DB_Template(uid):
    DB_Template = {
        'uid' : uid,
        'ToDoList':{
            'todolist' : [],
            'user_status' : {
                'FUNC_push' : False,
                'FUNC_delete' : False
            }
        },
        'RanDom':{
            'setlist':{
                #'class' : 'a to b'
            },
            'user_status':{
                'FUNC_push' : False,
                'FUNC_delete' : False,
                'FUNC_chose' : False,
                'FUNC_special' : True
            },
            'now_set' : '-1'
        },
        'nickname' : 'nickname'
    }
    return DB_Template
