def createAddTaskForm(parentProject=None):
    task = Database.Task()
    task.project_id = parentProject
    return createAddEditTaskForm(task)

def createEditTaskForm(taskId):
    session = Database.Session()
    T = Database.Task
    q = session.query(T).filter(T.task_id == taskId)
    task = q.one()
    return createAddEditTaskForm(task)

def createAddEditTaskForm(task):
    session = Database.Session()

    P = Database.Project

    projects = session.query(P).filter_by(project_status='active').order_by(P.project_name)

    Form = createFormContructor(task, projects)
    form = Form()
    return form

def receiveAddEditTaskForm():
    session = Database.Session()
    T = Database.Task
    t = T()
    Form = createFormContructor(t, [])
    f = Form()

    if f.validates():
        if f.d.task_id == "new":
            t = T()
        else:
            q = session.query(T).filter(T.task_id == int(f.d.task_id))
            t = q.one()
        t.task_name = f.d.task_name
        t.task_status = f.d.task_status
        t.project_id = int(f.d.task_project)
        if t.task_id == None:
            session.add(t)
        session.commit()

        if f.d.task_time_estimate != "":
            t_est = Database.TaskTimeEst()
            t_est.task_id = t.task_id
            t_est.task_time_estimate = f.d.task_time_estimate
            session.add(t_est)
            session.commit()
        return f.d.task_project

