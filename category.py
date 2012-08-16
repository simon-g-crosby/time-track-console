def category_mod_form():
    form = web.form.Form(
        web.form.Textbox('cat_name', web.form.notnull, 
                         description="Category Name:"),
        web.form.Button('Add todo'),


