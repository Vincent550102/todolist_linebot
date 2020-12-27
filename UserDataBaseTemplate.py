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
        'random':{
            'setlist':{
                
            }
        },
        'nickname' : 'nickname'
    }
    return DB_Template
