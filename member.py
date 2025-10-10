from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import date

class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # --- Member Information ---
    name = fields.Char(string='Member Name', required=True, tracking=True)
    phone = fields.Char(string='Phone Number')
    national_id = fields.Char(string='National ID Number')
    
    # --- Plan & Dates ---
    plan_type = fields.Selection([
        ('daily', 'Daily Pass'),
        ('monthly', 'Monthly Plan'),
        ('quarterly', 'Quarterly Plan'),
        ('annual', 'Annual Plan'),
    ], string='Subscription Plan', default='monthly', required=True, tracking=True)
    
    start_date = fields.Date(string='Start Date', default=fields.Date.today, required=True, tracking=True)
    
    # Computed fields for duration and status
    end_date = fields.Date(string='End Date', compute='_compute_dates_and_status', store=True, tracking=True)
    
    status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired')
    ], string='Status', compute='_compute_dates_and_status', store=True, tracking=True)

    # --- Compute Methods ---
    
    @api.depends('plan_type', 'start_date')
    def _compute_dates_and_status(self):
        """Calculates the end date based on the plan and determines the active status."""
        today = date.today()
        for member in self:
            end = member.start_date
            
            if member.start_date and member.plan_type:
                # Calculate End Date using relative delta
                if member.plan_type == 'daily':
                    end = member.start_date + relativedelta(days=1)
                elif member.plan_type == 'monthly':
                    end = member.start_date + relativedelta(months=1)
                elif member.plan_type == 'quarterly':
                    end = member.start_date + relativedelta(months=3)
                elif member.plan_type == 'annual':
                    end = member.start_date + relativedelta(years=1)
            
            member.end_date = end
            
            # Set Status
            if member.end_date and today <= member.end_date:
                member.status = 'active'
            else:
                member.status = 'expired'