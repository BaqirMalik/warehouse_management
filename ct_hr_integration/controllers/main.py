import base64

from odoo import http, SUPERUSER_ID
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class FetchJobApplications(http.Controller):
    @http.route('/fetch_job_application', type='http', auth='none',method=['GET','POST'], csrf=False)
    def fetch_job_application(self, **kw):
        headers_json = {'Content-Type': 'application/json'}
        try:
            # Extract data fields from request parameters
            career_id = int(kw.get('career_id'))
            first_name = kw.get('first_name')
            phone = kw.get('phone')
            email = kw.get('email')
            description = kw.get('description')
            file_data = kw.get('file')

            # Find the job position related to the career_id
            job_position = request.env['hr.job'].sudo().browse(career_id)

            if not job_position:
                _logger.error(f"Job position not found for career_id: {career_id}")
                return "Job position not found"

            # Create an hr.applicant record
            Applicant = request.env['hr.applicant'].with_user(SUPERUSER_ID)
            vals = {
                'name': job_position.name,
                'job_id': job_position.id,
                'partner_name': first_name,
                'partner_phone': phone,
                'email_from': email,
                'description': description,
            }
            new_applicant = Applicant.sudo().create(vals)

            # Optionally handle file upload (if file_data is provided)
            if file_data:
                # Ensure file_data is extracted correctly (example for Flask/Werkzeug)
                attachment_data = file_data.read()  # Read file content from FileStorage object

                # Process file_data to create an attachment
                attachment_vals = {
                    'name': file_data.filename,  # Filename of the uploaded file
                    'datas': base64.b64encode(attachment_data),  # Store the attachment data
                    'res_model': 'hr.applicant',  # Model to which the attachment is linked
                    'res_id': new_applicant.id,  # ID of the applicant record
                }
                attachment = http.request.env['ir.attachment'].sudo().create(attachment_vals)

        except Exception as e:
            _logger.error(f"Error creating applicant: {e}")
            return f"Error creating applicant: {e}"

        if new_applicant:
            response_data = {
                'id': new_applicant.id,
                'message': 'Record created successfully',
            }
        return Response(json.dumps(response_data), headers=headers_json)
