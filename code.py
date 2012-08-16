import web
import view
import CrudForms
from view import render
import Database
import urllib
import web_helper_functions
import os

from sqlalchemy import or_
from datetime import date

# def main():
#     db = DB()
#     session = db.createSession()

#     projects = session.query(Project).filter(Project.project_status=='active').order_by(Project.project_name)
        
#     formConstructor = createFormContructor("task", None, projects, None)
#     form = formConstructor()
#     print form.render()

# if __name__ == '__main__':
#     main()

urls = (
    '/', 'index',
    '/categories', 'categories',
    '/add_category', 'add_category',
    '/edit_category', 'edit_category',
    '/view_category', 'view_category',
    '/add_project', 'add_project',
    '/edit_project', 'edit_project',
    '/view_project', 'view_project',
    '/edit_project_due_date', 'edit_project_due_date',
    '/add_task', 'add_task',
    '/edit_task', 'edit_task',
    '/issues', 'issues',
    '/add_jog', 'add_jog',
    '/regen_reports','regen_reports',
    '/time_block_viewer', 'time_block_viewer'
)

class index:
    def GET(self):
        return render.base()

class categories:
    def GET(self):
        C = Database.Category
        session = Database.Session()
        categories = session.query(C)\
            .filter(or_(C.category_status == 'active',
                        C.category_status == 'inactive'))\
            .order_by(C.category_name).all()

        return render.categories(categories)

class add_category:
    def GET(self):
        form = CrudForms.createAddEditCategoryForm(None)
        return render.mod_category("Add", "add_category", form)

    def POST(self):
        CrudForms.receiveAddEditCategoryForm()
        return render.back_to_categories()

class edit_category:    
    def GET(self):
        user_data = web.input()
        categoryId = user_data['category_id']
        
        form = CrudForms.createAddEditCategoryForm(categoryId)
        return render.mod_category("Edit", "edit_category", form)

    def POST(self):
        catId = CrudForms.receiveAddEditCategoryForm()
        return render.back_to_category(catId)

class view_category:    
    def GET(self):
        user_data = web.input()
        categoryId = user_data['category_id']

        show_statuses = []
        if user_data.has_key('show_active'):
            show_statuses.append('show_active')
        if user_data.has_key('show_inactive'):
            show_statuses.append('show_inactive')
        if user_data.has_key('show_complete'):
            show_statuses.append('show_complete')
        if user_data.has_key('show_canceled'):
            show_statuses.append('show_canceled')        

        session = Database.Session()
        C = Database.Category
        category = session.query(C).filter_by(category_id=categoryId).one()
        categoryPageData = Database.loadCategoryPageData(categoryId,
                                                         show_statuses)   
        return render.view_category(category, categoryPageData,show_statuses)

class view_category_tasks:    
    def GET(self):
        user_data = web.input()
        categoryId = user_data['category_id']

        show_statuses = []
        if user_data.has_key('show_active'):
            show_statuses.append('show_active')
        if user_data.has_key('show_inactive'):
            show_statuses.append('show_inactive')
        if user_data.has_key('show_complete'):
            show_statuses.append('show_complete')
        if user_data.has_key('show_canceled'):
            show_statuses.append('show_canceled')        

        session = Database.Session()
        C = Database.Category
        category = session.query(C).filter_by(category_id=categoryId).one()
        categoryPageData = Database.loadCategoryPageData(categoryId,
                                                         show_statuses)   
        return render.view_category(category, categoryPageData,show_statuses)



class add_project:
    def GET(self):        
        form = CrudForms.createAddEditProjectForm(None)
        return render.mod_project("Add", "add_project", form)

    def POST(self):
        projectId = CrudForms.receiveAddEditProjectForm()
        return render.back_to_project(projectId)

class edit_project:    
    def GET(self):
        user_data = web.input()
        projectId = user_data['project_id']
        
        form = CrudForms.createAddEditProjectForm(projectId)
        return render.mod_project("Edit", "edit_project", form)

    def POST(self):
        projectId = CrudForms.receiveAddEditProjectForm()
        return web_helper_functions.redirectTo("view_project",
                                               {'project_id' : projectId,
                                                'show_active' : 'on'})

class edit_project_due_date:    
    def GET(self):
        user_data = web.input()
        projectId = user_data['project_id']
        projectDueDate = Database.getProjectDueDate(projectId)        
        return render.edit_project_due_date(projectId,projectDueDate)

    def POST(self):
        user_data = web.input()
        projectId = user_data['project_id']
        dueDate = user_data['due_date']

        Database.setProjectDueDate(projectId,dueDate) 

        return web_helper_functions.redirectTo("view_project",
                                               {'project_id' : projectId,
                                                'show_active' : 'on'})


class view_project:    
    def GET(self):
        user_data = web.input()
        projectId = user_data['project_id']

        show_statuses = []
        if user_data.has_key('show_active'):
            show_statuses.append('show_active')
        if user_data.has_key('show_inactive'):
            show_statuses.append('show_inactive')
        if user_data.has_key('show_complete'):
            show_statuses.append('show_complete')
        if user_data.has_key('show_canceled'):
            show_statuses.append('show_canceled')
        

        session = Database.Session()
        
        project = Database.getProject(projectId)

        projectTasks = Database.loadProjectPageData(projectId, show_statuses)
        
        
        PWP = Database.ProjectWikiPage
        pwp = session.query(PWP.project_wiki_page).filter_by(project_id=projectId).scalar()

        return render.view_project(project, projectTasks, pwp, show_statuses)


class tasks:
    def GET(self):
        session = Database.Session() 
        T = Database.Task
        tasks = session.query(T)\
            .filter(or_(T.task_status == 'active',T.task_status == 'inactive'))\
            .order_by(T.task_name).all()
        return render.tasks(tasks)

class add_task:
    def GET(self):
        user_data = web.input()
        projectId = user_data['project_id']
        
        form = CrudForms.createAddTaskForm(parentProject=projectId)
        return render.mod_task("Add", "add_task", form)

    def POST(self):
        projectId = CrudForms.receiveAddEditTaskForm()                
        return render.back_to_project(projectId)

class edit_task:    
    def GET(self):
        user_data = web.input()
        taskId = user_data['task_id']
        form = CrudForms.createEditTaskForm(taskId)
        return render.mod_task("Edit", "edit_task", form)

    def POST(self):
        projectId = CrudForms.receiveAddEditTaskForm()
        return render.back_to_project(projectId)

class issues:
    def GET(self):
        user_data = web.input()
        issue_id = user_data.get('issue_id', None)
        after_timestamp = user_data.get('after_timestamp', None)
        after_issue_id  = user_data.get('after_id', None)
        
        if after_timestamp != None and after_issue_id != None:
            issue = Database.loadNextUndeltwithIssueAfter(after_timestamp, after_issue_id)
        elif issue_id != None:            
            issue = Database.fetchIssue(issue_id)
        else:
            issue = Database.loadFirstUndeltwithIssue()

        if issue != None:
            return render.inbox_issue_view(issue,self.nextIssueUrl(issue))
        else:
            return render.inbox_issue_no_more_issues()

    def POST(self):
        user_data = web.input()
        issue_id = user_data.get('issue_id', None)
        remind_issue_id = user_data.get('remind_issue_id', None)
        remind_days = user_data.get('remind_days', 0)

        deltWith = user_data.get('delt_with', False)
        print "in post ", user_data

        if remind_issue_id != None:
            issue = Database.fetchIssue(remind_issue_id)            
            afterTs = issue.issue_timestamp
            Database.issuePostpone(remind_issue_id, remind_days)

            getParams = {'after_timestamp' : afterTs}

            return web_helper_functions.redirectTo('issues', getParams)

        if issue_id != None:
            Database.issueSetDeltWith(int(issue_id), deltWith)
            return render.back_to_issue(issue_id)
        

    def nextIssueUrl(self, issue):
        params = {'after_id' : issue.issue_id,
                  'after_timestamp' : issue.issue_timestamp }
        
        nextIssueUrl = "issues?" + urllib.urlencode(params)
        return nextIssueUrl


class add_jog:
    def GET(self):
        d = date.today()
        clist = Database.get_jogging_course_list()
        cdict = {}
        for i in clist:
            urlQuoted = urllib.quote_plus(i)
            cdict[urlQuoted] = i
        return render.add_jog(cdict,d.isoformat())

    def POST(self):
        user_data = web.input()

        course_name = user_data.get('course_name', None)
        isodate = user_data.get('date', None)

        time_hours = int(user_data.get('time_hours', 0))
        time_mins = int(user_data.get('time_mins', 0))
        time_secs = int(user_data.get('time_secs', 0))
        

        if (course_name == None or isodate == None):
            return None
        else:
            course_name = urllib.unquote_plus(course_name)
            seconds = ((time_hours * 60) + time_mins * 60) + time_secs   
            Database.add_jogging_run(isodate, seconds, course_name)
            return render.back_to_base()

class time_block_viewer:
    def GET(self):        
        user_data = web.input()
        todayDateIso = date.today().isoformat()
        d = user_data.get('date', todayDateIso)

        tbTable = Database.get_date_timeblocks(d)

        return render.time_block_viewer(tbTable)


            
class regen_reports:
    def GET(self):
        os.system("/bin/sh /home/simon/sshot/report_gen_scripts/all_scripts.sh")
        return web_helper_functions.redirectTo("/")

            

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
