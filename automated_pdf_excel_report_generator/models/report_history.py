from odoo import api, fields, models


class RgrReportHistory(models.Model):
    _name = 'rgr.report.history'
    _description = 'Report History'
    _inherit = ['mail.thread']
    _order = 'generated_date desc, id desc'

    name = fields.Char(string='History Name', required=True, tracking=True)
    template_id = fields.Many2one(
        comodel_name='rgr.report.template',
        string='Report Template',
        required=True,
        ondelete='restrict',
        tracking=True,
    )
    job_id = fields.Many2one(
        comodel_name='rgr.report.job',
        string='Generation Job',
        ondelete='set null',
        tracking=True,
    )
    file_name = fields.Char(string='File Name', readonly=True)
    file_size = fields.Integer(
        string='File Size (bytes)',
        readonly=True,
    )
    generated_date = fields.Datetime(
        string='Generated Date',
        default=fields.Datetime.now,
        readonly=True,
    )
    downloaded_by = fields.Many2one(
        comodel_name='res.users',
        string='Downloaded By',
        readonly=True,
    )
    download_count = fields.Integer(
        string='Download Count',
        default=0,
        readonly=True,
    )

    def action_download(self):
        """Download the file from the related generation job."""
        self.ensure_one()
        if self.job_id:
            self.sudo().write({
                'downloaded_by': self.env.user.id,
                'download_count': self.download_count + 1,
            })
            return self.job_id.action_download()
        return False
