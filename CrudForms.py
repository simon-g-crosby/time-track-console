from web.form import Form, Textbox, Dropdown, Hidden, Button, notnull
import Database

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



def createFormContructor(entity, possibleParentEntitiesList): 
    entityTypeName = entity.getTableName()
    entityId   = entity.getId()

    entityTypeParents = {"category" : None,
                         "project"  : "category",
                         "task"     : "project" }
    
    entityTypeParent = entityTypeParents[entityTypeName];

    if entityId == None :
        addOrEdit = "Add"
        entityIdStr = "new"
    else:
        addOrEdit = "Edit"
        entityIdStr = str(entityId)

    # fe abbrev for Form Elements
    fe = []

    fe.append(Textbox(entityTypeName + '_name',
                      notnull, 
                      description=entityTypeName.capitalize() + " Name:",
                      value=entity.getName()))

    if entityTypeParent != None:
        parentDropdownOpts = [(str(i.getId()), i.getName()) 
                              for i in possibleParentEntitiesList]
        fe.append(Dropdown(entityTypeName + '_' + entityTypeParent,
                           parentDropdownOpts,
                           description=entityTypeParent.capitalize(),
                           value=str(entity.getParentId())
                           ))
                  
    fe.append(Dropdown(entityTypeName + '_status', 
                       [('active', 'Active'),
                        ('inactive', 'Inactive'),
                        ('complete', 'Complete'),
                        ('canceled', 'Canceled')]))


    if entityTypeName != "category":
        fe.append(Textbox(entityTypeName + '_time_estimate',
                          description="Time Estimate (hours): ",
                          ))
        

    fe.append(Hidden(name=entityTypeName + '_id',
                     value=entityIdStr)),
    
    fe.append(Button(addOrEdit + ' ' + entityTypeName))

    return Form(*fe)
        

def createAddEditProjectForm(projectId):
    session = Database.Session()

    C = Database.Category
    P = Database.Project
    
    categories = session.query(C).filter_by(category_status='active').order_by(C.category_name)

    if projectId == None:
        project = P()
    else:
        q = session.query(P).filter(P.project_id == projectId)
        project = q.one()

    Form = createFormContructor(project, categories)
    form = Form()
    return form


def receiveAddEditProjectForm():
    session = Database.Session()
    P = Database.Project
    p = P()
    Form = createFormContructor(p, [])
    f = Form()

    if f.validates():
        if f.d.project_id == "new":
            p = P()
        else:
            q = session.query(P).filter(P.project_id == int(f.d.project_id))
            p = q.one()
        p.project_name = f.d.project_name
        p.project_status = f.d.project_status
        p.category_id = int(f.d.project_category)
        if p.project_id == None:
            session.add(p)
        session.commit()

        if f.d.project_time_estimate != "":
            p_est = Database.ProjectTimeEst()
            p_est.project_id = p.project_id
            p_est.project_time_estimate = f.d.project_time_estimate
            session.add(p_est)
            session.commit()
    return p.project_id


def createAddEditCategoryForm(categoryId):
    session = Database.Session()

    C = Database.Category
    
    if categoryId == None:
        category = C()
    else:
        q = session.query(C).filter(C.category_id == categoryId)
        category = q.one()

    Form = createFormContructor(category, None)
    form = Form()
    return form


def receiveAddEditCategoryForm():
    session = Database.Session()
    C = Database.Category
    c = C()

    Form = createFormContructor(c, [])
    f = Form()

    if f.validates():
        if f.d.category_id == "new":
            c = C()
        else:
            q = session.query(C).filter(C.category_id == int(f.d.category_id))
            c = q.one()
        c.category_name = f.d.category_name
        c.category_status = f.d.category_status

        if c.category_id == None:
            session.add(c)
        session.commit()

    print f.d.category_id
    return f.d.category_id
