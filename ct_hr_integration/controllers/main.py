from odoo import http
from odoo.http import request
import json

class WebhookController(http.Controller):

    @http.route('/fetch_job_application', type='http', auth='none', methods=['GET'], csrf=False)
    def receive_webhook(self, **kw):
        # Handle the webhook data here
        id = kw.get('id')
        if id:
            # Return a response indicating successful processing
            return json.dumps({'success': True})
        else:
            # Handle cases where no data is received
            return json.dumps({'success': False, 'error': 'ID is Mandatory'})
