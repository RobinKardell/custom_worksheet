{
    'name': 'Custom Worksheet',
    'version': '16.0.1.0.0',
    'category': 'Operations',
    'summary': 'Manage worksheets with customer links, reporting, and flexible statuses.',
    'author': 'Your Name',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/worksheet_views.xml',
        'views/worksheet_status_views.xml',
        'report/worksheet_report_templates.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
