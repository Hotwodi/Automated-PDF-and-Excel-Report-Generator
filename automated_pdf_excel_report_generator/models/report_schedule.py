from odoo import api, fields, models


class RgrReportSchedule(models.Model):
    _name = 'rgr.report.schedule'
    _description = 'Scheduled Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'next_run'

    name = fields.Char(string='Schedule Name', required=True, tracking=True)
    template_id = fields.Many2one(
        comodel_name='rgr.report.template',
        string='Report Template',
        required=True,
        ondelete='restrict',
        tracking=True,
    )
    cron_expression = fields.Char(
        string='Cron Expression',
        tracking=True,
        help='Standard cron expression describing the recurrence.',
    )
    next_run = fields.Datetime(
        string='Next Run',
        tracking=True,
    )
    last_run = fields.Datetime(
        string='Last Run',
        readonly=True,
        copy=False,
    )
    email_recipients = fields.Char(
        string='Email Recipients',
        help='Comma-separated list of email addresses to receive the report.',
    )
    active = fields.Boolean(string='Active', default=True, tracking=True)
    delivery_count = fields.Integer(
        string='Delivery Count',
        readonly=True,
        copy=False,
    )

    def action_run_now(self):
        """Trigger the linked template immediately and update schedule stats."""
        for schedule in self:
            if schedule.template_id:
                schedule.template_id.action_generate_report()
                schedule.write({
                    'last_run': fields.Datetime.now(),
                    'delivery_count': schedule.delivery_count + 1,
                })
                if schedule.next_run:
                    schedule._compute_next_run()
        return True

    @api.onchange('template_id')
    def _onchange_template_id(self):
        for schedule in self:
            if schedule.template_id and not schedule.name:
                schedule.name = '%s Schedule' % schedule.template_id.name

    def _compute_next_run(self):
        """Placeholder for next-run computation based on cron expression."""
        for schedule in self:
            if schedule.cron_expression:
                schedule.next_run = fields.Datetime.add(
                    fields.Datetime.now(), hours=24
                )
