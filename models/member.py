from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import date

class GymTrainee(models.Model):
    _name = 'gym.trainee'
    _description = 'Gym Trainee/Coach'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Coach Name', required=True, tracking=True)
    phone = fields.Char(string='Phone Number')
    national_id = fields.Char(string='National ID Number')
    
    image_1920 = fields.Image(string="Profile Picture", max_width=1920, max_height=1920, tracking=True)
    
    member_ids = fields.One2many(
        'gym.member', 
        'trainee_id', 
        string='Assigned Members'
    )
    
    member_count = fields.Integer(string='Member Count', compute='_compute_member_count', store=True)

    def _compute_member_count(self):
    
        for coach in self:
            coach.member_count = len(coach.member_ids)

class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Member Name', required=True, tracking=True)
    phone = fields.Char(string='Phone Number')
    national_id = fields.Char(string='National ID Number')
    
    trainee_id = fields.Many2one(
        'gym.trainee', 
        string='Assigned Coach', 
        tracking=True
    )
    
    plan_type = fields.Selection([
        ('daily', 'Daily Pass'),
        ('monthly', 'Monthly Plan'),
        ('quarterly', 'Quarterly Plan'),
        ('annual', 'Annual Plan'),
    ], string='Subscription Plan', default='monthly', required=True, tracking=True)
    
    start_date = fields.Date(string='Start Date', default=fields.Date.today, required=True, tracking=True)
    
    end_date = fields.Date(string='End Date', compute='_compute_dates_and_status', store=True, tracking=True)
    
    status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired')
    ], string='Status', compute='_compute_dates_and_status', store=True, tracking=True)

    
    @api.depends('plan_type', 'start_date')
    def _compute_dates_and_status(self):
        """Calculates the end date based on the plan and determines the active status."""
        today = date.today()
        for member in self:
            end = member.start_date
            
            if member.start_date and member.plan_type:
                if member.plan_type == 'daily':
                    end = member.start_date + relativedelta(days=1)
                elif member.plan_type == 'monthly':
                    end = member.start_date + relativedelta(months=1)
                elif member.plan_type == 'quarterly':
                    end = member.start_date + relativedelta(months=3)
                elif member.plan_type == 'annual':
                    end = member.start_date + relativedelta(years=1)
            
            member.end_date = end
        
            if member.end_date and today <= member.end_date:
                member.status = 'active'
            else:
                member.status = 'expired'
