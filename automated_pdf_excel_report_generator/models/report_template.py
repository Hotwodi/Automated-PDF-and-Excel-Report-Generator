from odoo import api, fields, models


class RgrReportTemplate(models.Model):
    _name = 'rgr.report.template'
    _description = 'Report Template'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(string='Template Name', required=True, tracking=True)
    model_name = fields.Char(
        string='Target Model',
        required=True,
        tracking=True,
        help='Technical name of the Odoo model to report on (e.g. sale.order).',
    )
    report_type = fields.Selection(
        selection=[
            ('pdf', 'PDF'),
            ('excel', 'Excel'),
            ('csv', 'CSV'),
        ],
        string='Report Type',
        required=True,
        default='pdf',
        tracking=True,
    )
    template_config = fields.Text(
        string='Template Configuration',
        help='JSON or YAML configuration describing columns, layout and styling.',
    )
    group_by = fields.Char(
        string='Group By',
        help='Comma-separated field paths used to group records in the report.',
    )
    filter_domain = fields.Text(
        string='Filter Domain',
        help='Odoo domain expression applied to the target model before export.',
    )
    schedule = fields.Selection(
        selection=[
            ('cron', 'Cron'),
            ('manual', 'Manual'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        string='Schedule',
        required=True,
        default='manual',
        tracking=True,
    )
    is_active = fields.Boolean(string='Active', default=True, tracking=True)
    last_generated = fields.Datetime(
        string='Last Generated',
        readonly=True,
        copy=False,
    )
    job_ids = fields.One2many(
        comodel_name='rgr.report.job',
        inverse_name='template_id',
        string='Generation Jobs',
    )
    schedule_ids = fields.One2many(
        comodel_name='rgr.report.schedule',
        inverse_name='template_id',
        string='Schedules',
    )
    history_ids = fields.One2many(
        comodel_name='rgr.report.history',
        inverse_name='template_id',
        string='History',
    )

    def action_generate_report(self):
        """Create and trigger a generation job for this template."""
        self.ensure_one()
        job = self.env['rgr.report.job'].create({
            'name': '%s - %s' % (self.name, fields.Datetime.now()),
            'template_id': self.id,
            'output_format': self.report_type,
            'state': 'draft',
            'generated_by': self.env.user.id,
        })
        job.action_run()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rgr.report.job',
            'res_id': job.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _log_generation(self):
        """Update last_generated timestamp after a report is produced."""
        self.write({'last_generated': fields.Datetime.now()})
