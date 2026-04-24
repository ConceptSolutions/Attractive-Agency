from odoo import http
from odoo.http import request, Response


class YamamahAgentController(http.Controller):

    @http.route(['/', '/home'], type='http', auth='public', website=True,
                    sitemap=False, save_session=False, multilang=True)
                        def homepage_agent_ready(self, **kwargs):
                                link_header = (
                                            '</.well-known/api-catalog>; rel="api-catalog", '
                                                        '</.well-known/agent-skills/index.json>; rel="agent-skills", '
                                                                    '</.well-known/mcp/server-card.json>; rel="mcp-server"'
                                                                            )
                                                                                    accept = request.httprequest.headers.get('Accept', '')
                                                                                            if 'text/markdown' in accept:
                                                                                                        md = '# Yamamah Smart SIS\n\nLeading acoustic engineering.\n'
                                                                                                                    return Response(md, content_type='text/markdown; charset=utf-8',
                                                                                                                                    headers={'Link': link_header, 'Vary': 'Accept'})
                                                                                                                                            website = request.env['website'].get_current_website()
                                                                                                                                                    response = website._serve_page()
                                                                                                                                                            if response and hasattr(response, 'headers'):
                                                                                                                                                                        response.headers['Link'] = link_header
                                                                                                                                                                                    response.headers['Vary'] = 'Accept'
                                                                                                                                                                                            return response
