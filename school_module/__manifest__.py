{
    'name': 'School Module',
    'version': '16.0.0.1',
    'category': 'Education/School',
    'website': 'https://leetcode.com/',
    'description': """
    This is my School Module which is used for create students.
    """,
    'depends':['crm','sale','web','mail','account','website','auth_signup'],
    
    'data':[
        'security/ir.model.access.csv',
        'views/student_detail.xml',
        'views/web_student_form.xml',
        'views/popup_view.xml',
        'views/mail_template.xml',
        'views/admission_detail.xml',
        'report/school_student_report.xml',
        'report/school_student_template.xml',
        'report/special_report.xml',
     
    ],
    'assets':{
        'web.assets_frontend': [
            '/school_module/static/src/js/addline.js',
            '/school_module/static/src/js/checkemail.js',
            # 'school_module/static/src/js/myMedia.js',
            '/school_module/static/src/scss/custom.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True, #An application module typically represents a functional part of the system and may introduce new menus, workflows, or features
}
