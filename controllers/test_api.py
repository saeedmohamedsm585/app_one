from odoo import http


class TestApi(http.Controller):

    @http.route("/api/test",methods=["GET"],type="http",auth="none",csrf=False)
    def test_endpoint(self):
        print("inside test_endpoint method")

    # @http.route('/api/test', type='json', auth='none', methods=['POST'], csrf=False)
    # def test_api(self, **kwargs):
    #     return {"message": "API is working"}