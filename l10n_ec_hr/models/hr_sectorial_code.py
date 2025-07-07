import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class HrSectorialCode(models.Model):
    _name = "hr.sectorial.code"
    _description = "Sectorial Code"

    iess_code = fields.Char(string="IESS Code", required=True)
    job_worker = fields.Char(string="Job")
    ocupational_structure = fields.Char()
    detail_job = fields.Char()
    wage = fields.Float(digits=(16, 4))

    @api.depends("iess_code", "job_worker")
    def _compute_display_name(self):
        for model in self:
            new_name = f"{model.iess_code} ({model.job_worker})"
            model.display_name = new_name

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("iess_code", operator, name),
                ("job_worker", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
