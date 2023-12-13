{
    'name': 'Token Module',
    'version': '16.0.0.1',
    'category': 'Custom/Token Module',
    'website': 'https://www.odoo.com/',
    'description': """
    This module is generate a link.Using this link you can download a pdf from anywhere.
    """,
    'depends':['account'],
    
    'data':[
    ],
    'assets':{
        'web.assets_frontend': [
            
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True, #An application module typically represents a functional part of the system and may introduce new menus, workflows, or features
}
