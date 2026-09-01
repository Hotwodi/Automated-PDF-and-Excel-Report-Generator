{
    'name': 'Automated PDF/Excel Report Generator',
    'version': '18.0.1.0.0',
    'images': ['static/description/cover.png'],
    'summary': 'Generate PDF, Excel and CSV reports on demand or on a schedule',
    'description': """
Automated PDF/Excel Report Generator
====================================
Create reusable report templates for any Odoo model, generate PDF, Excel
or CSV output on demand, and schedule recurring deliveries by email.
""",
    'author': 'SoftaiDev',
    'website': 'https://softaidev.pages.dev',
    'category': 'Productivity/AI',
    'license': 'LGPL-3',
    'price': 39.99,
    'currency': 'USD',
    'depends': ['base', 'web', 'mail'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/report_template_views.xml',
        'views/report_job_views.xml',
        'views/report_schedule_views.xml',
        'views/report_history_views.xml',
        'views/menu.xml',
    ],
}
