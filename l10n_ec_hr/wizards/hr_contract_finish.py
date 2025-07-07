from odoo import fields, models


class HrContractFinish(models.TransientModel):
    """Hr Contract Finish"""

    _name = "hr.contract.finish"
    _description = "Hr Contract Finish"

    contract_id = fields.Many2one(
        "hr.contract",
        string="Contract",
        default=lambda self: self._context.get("active_id"),
    )
    reason_id = fields.Many2one(
        "hr.contract.finish.reason", string="Finish Reason", required=True
    )
    employee = fields.Boolean(string="Archive Employee")
    date = fields.Date("Finish Date", required=True)

    def close(self):
        if self.contract_id.employee_id.active:
            self.contract_id.employee_id.update({"state": "inactive"})
        actual = self.mapped("contract_id.employee_id.work_period_ids").filtered(
            lambda x: x.contract_id == self.contract_id and x.period_type == "current"
        )
        if actual:
            actual.write({"period_type": "past", "date_end": self.date})
        self.contract_id.update(
            {"reason_id": self.reason_id.id, "date_end": self.date, "state": "close"}
        )
