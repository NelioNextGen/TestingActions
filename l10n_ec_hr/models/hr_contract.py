from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrContractType(models.Model):
    _inherit = "hr.contract.type"

    code = fields.Char()
    country_id = fields.Many2one("res.country", string="Country")
    antiquity = fields.Boolean()
    internship = fields.Boolean()


class HrContractFinishReason(models.Model):
    _name = "hr.contract.finish.reason"
    _description = "Contract Finish Reason"

    name = fields.Char(required=True)
    description = fields.Text()


class HrContract(models.Model):
    _inherit = "hr.contract"

    reason_id = fields.Many2one(
        "hr.contract.finish.reason", string="Contract Finish Reason"
    )
    job_ids = fields.One2many("hr.contract.job", "contract_id", string="Job History")
    wage_ids = fields.One2many("hr.contract.wage", "contract_id", string="Wage History")

    def contract_finish(self):
        form = self.env.ref("l10n_ec_hr.view_hr_contract_finish_reason", False)
        return {
            "name": _(f"Finish Contract for {self.employee_id.name}"),
            "type": "ir.actions.act_window",
            "res_model": "hr.contract.finish",
            "view_id": form.id,
            "view_mode": "form",
            "target": "new",
        }

    @api.constrains("employee_id", "date_start", "state")
    def _validation_only_contract_for_employee(self):
        for rec in self:
            contract_ids = self.env["hr.contract"].search_count(
                [
                    ("employee_id", "=", rec.employee_id.id),
                    ("id", "!=", rec.id),
                    ("state", "=", "open"),
                ]
            )
            if contract_ids != 0:
                raise UserError(_("you can only have one active contract per employee"))
            if not self.env["hr.employee.work.period"].search(
                [("contract_id", "=", rec.id)]
            ):
                rec.create_worker_period()

    def create_worker_period(self):
        for row in self:
            if row.employee_id.state == "inactive":
                row.employee_id.state = "active"
            row.employee_id.work_period_ids.create(
                {
                    "employee_id": row.employee_id.id,
                    "period_type": "current",
                    "contract_id": row.id,
                    "date_start": row.date_start,
                    "date_end": row.date_end,
                }
            )

    @api.onchange("date_end", "date_start")
    def _onchange_date(self):
        for rec in self:
            worker_id = self.env["hr.employee.work.period"].search(
                [("contract_id", "=", rec._origin.id)]
            )
            if worker_id:
                worker_id.write(
                    {"date_start": rec.date_start, "date_end": rec.date_end}
                )

    def unlink(self):
        for rec in self:
            worker_id = self.env["hr.employee.work.period"].search(
                [("contract_id", "=", rec.id)]
            )
            if worker_id:
                raise UserError(
                    _("Cannot delete a contract that has an active period!")
                )
        return super().unlink()


class HrContractJob(models.Model):
    """
    Historical record of job changes
    """

    _name = "hr.contract.job"
    _description = "Contract Job History"
    _order = "date"

    name = fields.Char("Reason")
    contract_id = fields.Many2one("hr.contract", string="Contract")
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        related="contract_id.employee_id",
        store=True,
    )
    old_job_id = fields.Many2one("hr.job", string="Old Job")
    job_id = fields.Many2one("hr.job", string="Job")
    date_from = fields.Date("From")
    date_to = fields.Date("To")
    date = fields.Date("Update Date")


class HrContractWage(models.Model):
    """
    Historical record of wage changes
    """

    _name = "hr.contract.wage"
    _description = "Contract Wage History"
    _order = "date"

    name = fields.Char("Reason")
    contract_id = fields.Many2one("hr.contract", string="Contract")
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        related="contract_id.employee_id",
        store=True,
    )
    old_wage = fields.Float()
    wage = fields.Float()
    date_from = fields.Date("From")
    date_to = fields.Date("To")
    date = fields.Date("Update Date")
