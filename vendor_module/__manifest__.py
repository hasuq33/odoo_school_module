{
    'name': 'My Contacts',
    'version': '16.0.0.1',
    'data':[
        'security/ir.model.access.csv',
        'views/vendor.xml'
    ],
    'depends':['contacts'],
      'installable': True,
      'auto_install': False,
      'application': True, #An application module typically represents a functional part of the system and may introduce new menus, workflows, or features
}