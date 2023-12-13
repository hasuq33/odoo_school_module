{
    'name': 'Media Module',
    'version': '16.0.0.1',
    'category': 'Media/User Media',
    'website': 'https://leetcode.com/',
    'description': """
    This module will save a record of media
    """,
    'depends':['base','web','website','auth_signup','mail'],
    
    'data':[
        'security/ir.model.access.csv',
        'views/myview.xml',
        'views/imageview.xml',
        'views/mail_template.xml',
        'views/webview.xml',
    ],
    'assets':{
        'web.assets_frontend': [
            '/media_module/static/src/js/script.js'
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True, #An application module typically represents a functional part of the system and may introduce new menus, workflows, or features
}
