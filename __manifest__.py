{
    'name': 'نادي المكنات الرياضي',
    'summary': 'تطبيقنا يُتيح لأعضاء النادي تسجيل الدخول لتتبع بياناتهم، ويُسجّل معلومات الأعضاء والمدربين بسهولة.',
    'description': 'Tracks member details, selected plan (Daily/Monthly/etc.), and automatically calculates expiration dates and status.',
    'author': 'Eltabri Mohammed, Ahmed Khalid, Ahmed Abbas',
    'version': '18.0.1.0.0',
    'category': 'رياضي',
    'depends': [
        'base',
        'mail', 
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/member_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
