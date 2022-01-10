# -*- coding: utf-8 -*-
{
    'name': "open_academy",
    'summary': """
        Open Academy exercise based on Odoo documentation:
        https://www.odoo.com/documentation/15.0/developer/howtos/backend.html?highlight=context#
    """,
    'description': """
        Module allowing to organize and handle an academy.
        New courses and sessions can be created and both instructors and attendees can be registered into them.
        A dashboard allows to visualize some statistics and a calendar view of all the sessions.
    """,
    'author': "Samuel Ciulla",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base', 
        'sale',
        'board',
    ],
    'data': [
        'data/res_groups.xml',
        'security/ir.model.access.csv',
        'views/open_academy_menu_views.xml',
        'views/open_academy_course_views.xml',
        'views/open_academy_session_views.xml',
        'views/open_academy_partner_views.xml',
        'views/open_academy_partner_fax_views.xml',
        'views/open_academy_sale_order_fax.xml',
        'views/open_academy_dashboard_views.xml',
        'wizard/set_attendees_views.xml',
        'report/open_academy_session_report_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
