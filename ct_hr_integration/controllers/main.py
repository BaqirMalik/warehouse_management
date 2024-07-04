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
            if 'crecentech_career_id' in kw and kw['crecentech_career_id']:
                crecentech_career_id = int(kw.get('crecentech_career_id'))
            else:
                response_data = {
                    'error': 'Crecentech Career id is Required',
                }
                return Response(json.dumps(response_data), headers=headers_json)

            if 'crecentech_career_name' in kw and kw['crecentech_career_name']:
                crecentech_career_name = kw.get('crecentech_career_name')
            else:
                response_data = {
                    'error': 'Crecentech Career Name is Required',
                }
                return Response(json.dumps(response_data), headers=headers_json)

            if 'first_name' in kw and kw['first_name']:
                first_name = kw.get('first_name')
            else:
                response_data = {
                    'error': 'Name is Required',
                }
                return Response(json.dumps(response_data), headers=headers_json)

            if 'phone' in kw and kw['phone']:
                phone = kw.get('phone')
            else:
                response_data = {
                    'error': 'Phone is Required',
                }
                return Response(json.dumps(response_data), headers=headers_json)

            if 'email' in kw and kw['email']:
                email = kw.get('email')
            else:
                response_data = {
                    'error': 'Email is Required',
                }
                return Response(json.dumps(response_data), headers=headers_json)

            if 'description' in kw and kw['description']:
                description = kw.get('description')
            else:
                response_data = {
                    'error': 'Description is Required',
                }
                return Response(json.dumps(response_data), headers=headers_json)

            file_data = kw.get('file')

            # Find the job position related to the career_id
            job_position = request.env['hr.job'].sudo().search([('crecentech_career_id','=',crecentech_career_id)],limit=1)

            if not job_position:
                _logger.error(f"Job position not found for Job Name: {crecentech_career_name}")
                response_data = {
                    'error': f"Job position not found for Job Name: {crecentech_career_name}",
                }
                return Response(json.dumps(response_data), headers=headers_json)

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
            if file_data:
                attachment_data = file_data.read()  # Read file content from FileStorage object
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