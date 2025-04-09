# -*- coding: utf-8 -*-
from builtins import print
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

from odoo import api, fields, models, tools, _
from odoo.tools.misc import xlwt
from odoo.exceptions import ValidationError, UserError
import io
import base64
import itertools


class ReportPayslips(models.TransientModel):
    _name = 'hr.payslip.salary'

    start_date = fields.Date(string="Start Date", required=True, )
    end_date = fields.Date(string="End Date", required=True, )
    employee_ids = fields.Many2many('hr.employee', string='Employee')
    dep_ids = fields.Many2many('hr.department', string='Department')
    struct_ids = fields.Many2many('hr.payroll.structure', string='Structure')
    hr_salary_rule_ids = fields.Many2many('hr.salary.rule', string='Salary Rules')
    hr_salary_rule_category_ids = fields.Many2many('hr.salary.rule.category', string='Salary Rules Category')
    excel_sheet = fields.Binary()
    company_id = fields.Many2one('res.company', string='company', required=True, default=lambda self: self.env.company)
    is_total = fields.Boolean()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done '),
        ('cancel', 'Cancelled'),
        ('paid', 'Paid'),
    ], string='Status', default='verify',)

    @api.onchange('struct_ids')
    def onchange_struct_ids(self):
        res = {}
        rules_ids = self.env['hr.salary.rule'].search([
            ('struct_id', 'in', self.struct_ids.ids),
            ('appears_on_payslip', '=', True)
        ])
        if len(rules_ids.ids) > 0:
            res['domain'] = {'hr_salary_rule_ids': [('id', 'in', rules_ids.ids)]}
        else:
            res['domain'] = {'hr_salary_rule_ids': [('id', '=', False)]}
        return res

    def print_report_excel(self):
        return self.env.ref('salary_report.salary_report_xlsx').report_action(self)

    def print_pdf_report(self):
        employee_ids = self.employee_ids.ids if self.employee_ids else self.env['hr.employee'].search([]).ids
        dep_ids = self.dep_ids.ids if self.dep_ids else self.env['hr.department'].search([]).ids
        struct_ids = self.struct_ids.ids if self.struct_ids else self.env['hr.payroll.structure'].search([]).ids
        hr_salary_rule_ids = self.hr_salary_rule_ids.ids if self.hr_salary_rule_ids else self.env[
            'hr.salary.rule'].search([]).ids
        print(">>>>>>>>xcxcx<<<<<<", self.hr_salary_rule_ids.ids)
        print(">>>>>>>>xcxcx<<<<<<", self.env['hr.salary.rule'].search([]).ids)

        domain = []
        if employee_ids:
            domain.append(('employee_id', 'in', employee_ids))
        elif dep_ids:
            domain.append(('employee_id.department_id', 'in', dep_ids))
        elif struct_ids:
            domain.append(('struct_id', 'in', struct_ids))
        elif self.start_date:
            domain.append(('date_from', '>=', self.start_date))
        elif self.end_date:
            domain.append(('date_to', '<=', self.end_date))
        elif self.state:
            domain.append(('state', '=', self.state))
        hr_payslip_ids = self.env['hr.payslip'].search(domain)

        categ_id = []
        for rec in hr_payslip_ids.line_ids:
            categ_id.append({
                'id': rec.category_id.id,
                "categ_id": rec.category_id,
                "amount": rec.amount
            })

        docs = sorted(categ_id, key=lambda i: (i['id']))

        lst = []
        i = 0
        for key, group in itertools.groupby(docs, key=lambda x: (x['id'])):
            print('keyyyyyyyyyyyyyyyy', key)
            print('groupppppppppp', group)
            line = []
            price_total = 0
            categ_id_2 = ''
            for item in group:
                categ_id_2 = item['categ_id']
                price_total += item["amount"]
            lst.append({
                'categ_id': categ_id_2,
                'id': categ_id_2.id,
                'name': categ_id_2.name,
                'amount': round(price_total, 2)

            })
        print("================", lst)

        # self.generate_xlsx_report(workbook, hr_payslip_ids)
        data = {
            'model': self,
            'ids': self.ids,
            'model': self._name,
            'report_name': 'SR',
            'form': {
                'date_from': self.start_date,
                'date_to': self.end_date,
                'hr_payslip_ids': hr_payslip_ids.ids,
                'struct_ids': struct_ids,
                'employee_ids': employee_ids,
                'hr_salary_rule_ids': hr_salary_rule_ids,
                'company_id': self.company_id.id,
                'lst': lst
            },
        }
        if len(hr_payslip_ids.ids) != 0:
            if self.is_total:
                return self.env.ref('salary_report.action_salary_total_report_pdf').report_action([], data=data)
            else:
                return self.env.ref('salary_report.action_salary_report_pdf').report_action([], data=data)

        else:
            raise ValidationError(' There is No Data to Show')

    def get_rule_data(self,cat):
       salary_rule_category_ids = self.env['hr.salary.rule.category'].search([('name', '=', cat)])
       print('salary_rule_category_ids',salary_rule_category_ids)
       rec= self.env['hr.payslip.line'].search([('category_id','=',salary_rule_category_ids.id)])
       print('recccccc', rec)
       total_basic = 0
       list_data = []
       list_basic = []
       total_alw=0
       list_alw=[]
       total_gross = 0
       list_gross = []
       total_dedu = 0
       list_dedu = []
       total_net = 0
       list_net = []
       for r in rec:

          if r.slip_id.date_from >= self.start_date and r.slip_id.date_to <= self.end_date:
              if r.slip_id.category_id == 'Basic':
                  print("Basiccccccccccccccc")
                  total_basic += r.amount
                  list_basic.append(r)
                  print('total_basic',total_basic)
                  print('list_basic',list_basic)
              elif r.slip_id.category_id == 'Allowance':
                  total_alw += r.amount
                  list_alw.append(r)
              elif r.slip_id.category_id == 'Gross':
                  total_gross += r.amount
                  list_gross.append(r)
              elif r.slip_id.category_id == 'Deduction':
                  total_dedu += r.amount
                  list_dedu.append(r)
              elif r.slip_id.category_id == 'Net':
                  total_net += r.amount
                  list_net.append(r)
              else:
                  print("Errorrrrrrrrrrrrrrrrrrrrrr")

       return {
           'list_basic':list_basic,
            'total_basic':total_basic,
            'list_alw':list_alw,
            'total_alw':total_alw,
            'list_gross':list_gross,
            'total_gross':total_gross,
            'list_dedu':list_dedu,
            'total_dedu':total_dedu,
            'list_net':list_net,
            'total_net':total_net,
       }

    def print_report(self):
        employee_ids = self.employee_ids.ids if self.employee_ids else self.env['hr.employee'].search([]).ids
        dep_ids = self.dep_ids.ids if self.dep_ids else self.env['hr.department'].search([]).ids
        struct_ids = self.struct_ids.ids if self.struct_ids else self.env['hr.payroll.structure'].search([]).ids
        hr_salary_rule_ids = self.hr_salary_rule_ids.ids if self.hr_salary_rule_ids else self.env['hr.salary.rule'].search([]).ids

        domain = []
        if employee_ids:
            domain.append(('employee_id', 'in', employee_ids))
        elif dep_ids:
            domain.append(('employee_id.department_id', 'in', dep_ids))
        elif struct_ids:
            domain.append(('struct_id', 'in', struct_ids))
        elif self.start_date:
            domain.append(('date_from', '>=', self.start_date))
        elif self.end_date:
            domain.append(('date_to', '<=', self.end_date))
        elif self.state:
            domain.append(('state', '=', self.state))
        hr_payslip_ids = self.env['hr.payslip'].search(domain)

        data = {
            'ids': self.ids,
            'model': self._name,
            'report_name': 'dddd',
            'form': {
                'date_from': self.start_date,
                'date_to': self.end_date,
                'hr_payslip_ids': hr_payslip_ids.ids,
                'struct_ids': struct_ids,
                'employee_ids': employee_ids,
                'hr_salary_rule_ids': hr_salary_rule_ids,
                'company_id': self.company_id.id,
            },
        }
        lines = self.env['hr.payslip'].browse(data["form"]['hr_payslip_ids'])
        if self.start_date and self.end_date:
            filename = 'SalaryReport from ' + str(self.start_date) + " to " + str(self.end_date) + '.xls'
        else:
            filename = 'SalaryReport.xls'
        workbook = xlwt.Workbook()

        worksheet = workbook.add_sheet(filename, cell_overwrite_ok=True)
        # for shx in 0, 1:
        #     worksheet.cols_right_to_left = shx
        font = xlwt.Font()
        font.bold = True

        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'


        # first_header = xlwt.easyxf(
        #     'font:color #A3C7F3, bold 0,font_size: 15; borders: top double, bottom double, left double, right double;'
        #     'align: vertical center, horizontal center, wrap yes;'
        # )
        title_format = xlwt.easyxf(
            "font: color black,height 300, bold True, name Arial; align: vertical center, horizontal center;"
            " borders: top double, bottom double, left double, right double;")
        table_header_format = xlwt.easyxf(
            "font: color black,height 200, bold True, name Arial; align: vertical center, horizontal center;"
            " borders: top double, bottom double, left double, right double;")
        custom_format = xlwt.easyxf(
            "font:color black, bold 0,height 200; borders: top thin, bottom thin, left thin, right thin;"
            "align: vertical center, horizontal center, wrap yes;"
        )

        # worksheet.write_merge(0, 1, 6, 8, 'Salary Report', table_header_format)
        salary_rule_ids = self.env['hr.salary.rule'].browse(data['form']['hr_salary_rule_ids']) if len(
            data['form']['hr_salary_rule_ids']) > 0 else self.env['hr.salary.rule'].search([], order='sequence asc')
        total_dict = {}
        datas = []
        company_id = self.env['res.company'].browse(data['form']['company_id'])
        # buf_image = io.BytesIO(base64.b64decode(company_id.logo))
        # worksheet.insert_image(0, 5, 'img.png', {'image_data': buf_image, 'x_scale': 0.10, 'y_scale': 0.10})

        worksheet.col(0).width = int(10 * 700)
        worksheet.col(1).width = int(10 * 700)
        worksheet.col(2).width = int(10 * 700)
        worksheet.col(3).width = int(10 * 700)
        worksheet.row(0).height = int(2 * 350)
        worksheet.row(2).height = int(2 * 350)

        if salary_rule_ids:
            row = 4
            worksheet.write(0,3, 'Salary Report', title_format)
            if self.start_date and self.end_date:
                text = 'Employee Salary from Date' + str(self.start_date) + " to " + str(self.end_date)
            worksheet.write_merge(2, 2, 0, 3, text, title_format)
            col = 0
            for rule in salary_rule_ids:
                worksheet.write(row, col, rule.name, table_header_format)
                total_dict.update({rule.id: 0})
            row += 1
            col = 2
            for slip in lines:
                line = {}
                row += 1
                for slip_line in slip.line_ids:
                    if slip_line.salary_rule_id.id in salary_rule_ids.ids:
                        line['ref'] = slip.number
                        line['code'] = slip.employee_id.pin if slip.employee_id.pin else ""
                        line['slip_name'] = slip.name
                        line['emp_name'] = slip.employee_id.name
                        line[
                            'bank_account_id'] = slip.employee_id.bank_account_id.acc_number if slip.employee_id.bank_account_id else ""
                        line['name'] = slip.employee_id.name
                        line['job'] = slip.employee_id.job_title
                        line[
                            'start_work'] = slip.employee_id.contract_id.date_start if slip.employee_id.contract_id else ""
                        line[
                            'department'] = slip.employee_id.contract_id.department_id.name if slip.employee_id.contract_id else ""
                        line['basic_salary'] = slip.basic_wage
                        line['allowance_wage'] = slip.allowance_wage
                        line['gross_wage'] = slip.gross_wage
                        line['deduction_wage'] = slip.deduction_wage
                        line['net_wage'] = slip.net_wage
                        if slip_line.amount > 0:
                            line[slip_line.salary_rule_id.id] = slip_line.amount
                            total_dict.update(
                                {slip_line.salary_rule_id.id: total_dict[
                                                                  slip_line.salary_rule_id.id] + slip_line.amount})
                datas.append(line)
            row += 1
            col = 2
            row = 4

            rules_ids = []
            for rl in total_dict:
                if total_dict[rl] > 0:
                    rules_ids.append(rl)
            sal_rule_ids = self.env['hr.salary.rule'].search([('id', 'in', rules_ids)], order='sequence asc')
            col = 0
            worksheet.write(row, col, "#", table_header_format)
            col += 1
            worksheet.write(row, col, "Ref", table_header_format)
            col += 1
            worksheet.write(row, col, "Code", table_header_format)
            col += 1
            worksheet.write(row, col, "Name", table_header_format)
            col += 1
            worksheet.write(row, col, "Job", table_header_format)
            col += 1
            worksheet.write(row, col, "Work Date", table_header_format)
            col += 1
            worksheet.write(row, col, "Department", table_header_format)
            col += 1
            # Header Line
            for sa_line in sal_rule_ids:
                worksheet.write(row, col, sa_line.name, table_header_format)
                col += 1
            # worksheet.write(row, col, "Bank NO", table_header_format)
            # col += 1
            row += 1
            ############  Report Lines  ###############
            count = 0
            for line in datas:
                col = 0
                count += 1
                worksheet.write(row, col, count, custom_format)
                col += 1
                worksheet.write(row, col, line.get('ref'), custom_format)
                col += 1
                worksheet.write(row, col, line.get('code'), custom_format)
                col += 1
                worksheet.write(row, col, line.get('name'), custom_format)
                col += 1
                worksheet.write(row, col, line.get('job'), custom_format)
                col += 1
                worksheet.write(row, col, line.get('start_work'), custom_format)
                col += 1
                worksheet.write(row, col, line.get('department'), custom_format)
                col += 1
                for sa_line in sal_rule_ids:
                    if sa_line.id in line.keys():
                        worksheet.write(row, col, line[sa_line.id], custom_format)
                    col += 1
                # worksheet.write(row, col, line['bank_account_id'], custom_format)
                # col += 1
                row += 1
            col = 7
            for sa_line in sal_rule_ids:
                for tot in total_dict:
                    if tot == sa_line.id:
                        worksheet.write(row, col, total_dict[tot], table_header_format)
                col += 1
            col += 1
            row += 1

        else:
            raise ValidationError(_('There is no Salary Rules !!'))

        fp = io.BytesIO()
        workbook.save(fp)
        report_id = self.env['excel.report.salary'].create({
            'excel_file': base64.encodebytes(fp.getvalue()),
            'file_name': filename
        })
        fp.close()

        if len(hr_payslip_ids.ids) > 0:
            return {
                'view_mode': 'form',
                'res_id': report_id.id,
                'res_model': 'excel.report.salary',
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        else:
            raise ValidationError(' There is No Data to Show')

    def formate_data_to_pdf(self, hr_payslip_ids, salary_rule_ids):
        lines = self.env['hr.payslip'].browse(hr_payslip_ids)
        salary_rule_ids = self.env['hr.salary.rule'].browse(salary_rule_ids) if  len(salary_rule_ids)>0 else self.env['hr.salary.rule'].search([], order='sequence asc')
        total_dict = {}
        datas = []

        allw_total = 0
        dedu_total = 0
        basic_total = 0
        gross_total = 0
        if salary_rule_ids:
            for rule in salary_rule_ids:
                total_dict.update({rule.id: 0})
                print('total_dict', total_dict)
            for slip in lines:
                # if slip.category_id != salary_rule_category_ids:
                #    continue
                line = {}
                for slip_line in slip.line_ids:
                    print(slip_line.salary_rule_id.id)
                    # if slip_line.salary_rule_id.id in salary_rule_ids.ids:
                    #     if slip.category_id.name=='Basic':
                    #         basic_total+=slip.basic_wage
                    #     if slip.category_id.name=='Allowance':
                    #         allw_total+=slip.allowance_wage

                    if slip_line.salary_rule_id.id == 15:
                        print(slip_line.salary_rule_id.name, '  1111 ', slip_line.amount)
                    line['ref'] = slip.number
                    line['code'] = slip.employee_id.pin if slip.employee_id.pin else ""
                    line['slip_name'] = slip.name
                    line['emp_name'] = slip.employee_id.name
                    line[
                        'bank_account_id'] = slip.employee_id.bank_account_id.acc_number if slip.employee_id.bank_account_id else ""
                    line['name'] = slip.employee_id.name
                    line['job'] = slip.employee_id.job_title
                    line['start_work'] = slip.employee_id.contract_id.date_start if slip.employee_id.contract_id else ""
                    line[
                        'department'] = slip.employee_id.contract_id.department_id.name if slip.employee_id.contract_id else ""
                    line['basic_salary'] = slip.basic_wage
                    line['allowance_wage'] = slip.allowance_wage
                    line['gross_wage'] = slip.gross_wage
                    line['deduction_wage'] = slip.deduction_wage
                    line['net_wage'] = slip.net_wage
                    if slip_line.amount != 0:
                        line[slip_line.salary_rule_id.id] = slip_line.amount
                        print(">>>>>>line<<", line)
                        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx", slip_line.amount)
                        if self.hr_salary_rule_ids:
                            for rule in self.hr_salary_rule_ids:
                                if rule.name == slip_line.salary_rule_id.name:
                                    total_dict.update({slip_line.salary_rule_id.id: total_dict[
                                                                                        slip_line.salary_rule_id.id] + slip_line.amount})
                        else:
                            total_dict.update({slip_line.salary_rule_id.id: total_dict[
                                                                                slip_line.salary_rule_id.id] + slip_line.amount})
                datas.append(line)

            rules_ids = []
            for rl in total_dict:
                if total_dict[rl] != 0:
                    rules_ids.append(rl)
            sal_rule_ids = self.env['hr.salary.rule'].search([('id', 'in', rules_ids)], order='sequence asc')

            count = 0
            for line in datas:
                col = 0
                count += 1
                for sa_line in sal_rule_ids:
                    if sa_line.id in line.keys():
                        pass
                        # Salary rule name
            for sa_line in sal_rule_ids:
                for tot in total_dict:
                    if tot == sa_line.id:
                        pass
                        # in XML
        print("finalllllllll ", rules_ids)
        return {
            'rules_ids': rules_ids,
            'all_data': datas,
            'total_dict': total_dict,
            'total_basic': basic_total,
            'total_allw': allw_total,
        }

