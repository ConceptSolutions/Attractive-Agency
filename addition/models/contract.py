from odoo import fields, models, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    hour_value = fields.Float(string='Hour Value', )
    worked_dys = fields.Float(string='hours Per Day', )
    day_value = fields.Float(string='Day Value', compute="get_day_value", store=True)
    # month_value = fields.Float(string='Month Value', compute="get_month_value", store=True)

    x_variable_salary = fields.Monetary(string="Variable Salary", required=False, )
    donations = fields.Monetary(string="Donations")
    job_speciality_allowance = fields.Monetary(string="Job Speciality Allowance")

    @api.depends('hour_value', 'worked_dys')
    def get_day_value(self):
        for rec in self:
            print(rec.hour_value, "           ", rec.worked_dys)
            rec.day_value = rec.hour_value * rec.worked_dys

    # @api.depends('wage', 'basic_plus')
    # def get_month_value(self):
    #     for rec in self:
    #         rec.month_value = rec.wage + rec.basic_plus
