from odoo import _, fields, models
from odoo.exceptions import UserError


class HrContractUpdate(models.TransientModel):
    """
    This wizard allows you to update the work order or the salary of an employee,
    either individually or by department
    """

    _name = "hr.contract.update"
    _description = "HR Contract Update"

    option = fields.Selection(
        [("wage", _("Wage Update")), ("job", _("Job Update"))],
        default="wage",
    )
    wage_ids = fields.One2many(
        "hr.contract.update.wage", "wiz_id", string="Update Wage"
    )
    job_ids = fields.One2many("hr.contract.update.job", "wiz_id", string="Update Job")

    def update_contract(self):
        wage_obj = self.env["hr.contract.wage"]
        for row in self:
            if row.option == "wage":
                if row.wage_ids:
                    for w in row.wage_ids:
                        if w.type == "increase":
                            if w.wage <= w.old_wage:
                                raise UserError(
                                    _(
                                        "The value of the new salary must be greater "
                                        "than the value of the previous salary"
                                    )
                                )
                        if w.type == "reduce":
                            if w.wage >= w.old_wage:
                                raise UserError(
                                    _(
                                        "The value of the new salary must be less"
                                        " than the value of the previous salary"
                                    )
                                )
                        old = wage_obj.search(
                            [
                                ("date_to", "<", w.date),
                                ("contract_id", "=", w.contract_id.id),
                            ],
                            limit=1,
                        )
                        if old:
                            date_from = old.date_to
                        else:
                            date_from = w.contract_id.date_start
                        wage_vals = {
                            "contract_id": w.contract_id.id,
                            "employee_id": w.contract_id.employee_id.id,
                            "date_from": date_from,
                            "date_to": w.date,
                            "date": fields.Date.today(),
                            "old_wage": w.old_wage,
                            "wage": w.wage,
                            "name": w.name,
                        }
                        w.contract_id.write({"wage": w.wage})
                        wage_obj.create(wage_vals)
                else:
                    raise UserError(
                        _(
                            "¡You must select at least one employee"
                            " to perform the wage update!"
                        )
                    )


class HrContractUpdateWage(models.TransientModel):
    _name = "hr.contract.update.wage"
    _description = "HR Contract Update Wage"

    wiz_id = fields.Many2one("hr.contract.update")
    contract_id = fields.Many2one("hr.contract", string="Contract")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    old_wage = fields.Float()
    wage = fields.Float("New Wage")
    type = fields.Selection([("increase", "Increase"), ("reduce", "Reduce")])
    date = fields.Date()
    name = fields.Char("Reason")


class HrContractUpdateJob(models.TransientModel):
    _name = "hr.contract.update.job"
    _description = "HR Contract Update Job"

    wiz_id = fields.Many2one("hr.contract.update")
    contract_id = fields.Many2one("hr.contract", string="Contract")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    old_job_id = fields.Many2one("hr.job", string="Old Job")
    job_id = fields.Many2one("hr.job", string="New Job")
    date = fields.Date()
    name = fields.Char("Reason")
