{
    'name': 'GymFlow Membership',
    'summary': 'Simple app to manage gym members and subscription plans.',
    'description': 'Tracks member details, selected plan (Daily/Monthly/etc.), and automatically calculates expiration dates and status.',
    'author': 'Your Team',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'depends': [
        'base',
        'mail', # ADDED: Required for mail.thread and mail.activity.mixin inheritance
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/member_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
