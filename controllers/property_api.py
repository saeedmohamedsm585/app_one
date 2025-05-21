import json
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request


def valid_response(data,stauts):
    response_body={
        'data':data,
        'message':"Successful"
    }
    return request.make_json_response(response_body, status=stauts)

def invalid_response(error,stauts):
    response_body={
        'error':error,
    }
    return request.make_json_response(response_body, status=stauts)


class PropertyApi(http.Controller):

    @http.route("/v1/property",methods=["POST"],type="http",auth="none",csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                "message" : "name is required"
            },status=400)

        try:
             res = request.env['property'].sudo().create(vals)
             #print(res) #property(41,)
             if res:
                 return request.make_json_response({
                  "messege" : "property has created successfuly",
                   "name" : res.name,
                    "id" : res.id

                        }, status=201)

        except Exception as error:
            return request.make_json_response ({
            "error":error,
        }, status=400)

    @http.route("/v1/json/property", methods=["POST"], type="json", auth="none", csrf=False)
    def json_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return ({
                "messege": "property has created successfuly",
                "name": res.name,
                "id": res.id

                    })

    @http.route("/v1/property/<int:propert_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self,propert_id):
        try:
           property_id = request.env['property'].sudo().search([('id','=',propert_id)])
           if not property_id:
               return invalid_response(  "ID does not exist" , 400)

           args = request.httprequest.data.decode()
           vals = json.loads(args)
           property_id.write(vals)
           return request.make_json_response({
            "messege": "property has updated successfuly",
            "name": property_id.name,
            "id": property_id.id
                 }, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/property/<int:propert_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, propert_id):
            try:
                property_id = request.env['property'].sudo().search([('id', '=', propert_id)])
                if not property_id:
                    return request.make_json_response({
                        "message": "ID does not exist"
                              }, status=400)
                return request.make_json_response({
                    "name": property_id.name,
                    "id": property_id.id,
                    "postcode": property_id.postcode,
                    "state": property_id.state
                }, status=200)

            except Exception as error:
                 return request.make_json_response({
                "error": error,
                 }, status=400)

    @http.route("/v1/property/<int:propert_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, propert_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', propert_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "ID does not exist"
                }, status=400)
            property_id.unlink()
            return request.make_json_response({
                "message": "property deleted successfly",
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_all_property(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            print(params) #{'state': ['sold']}
            property_domain = []
            if params.get('state'):
                property_domain +=[('state','=',params.get('state')[0])]
                print(property_domain) #[('state', '=', 'sold')]
            # property_ids = request.env['property'].sudo().search([]) get all Records
            property_ids = request.env['property'].sudo().search(property_domain)
            if not property_ids:
                return request.make_json_response({
                    "message": "ID does not exist"
                }, status=400)

            return valid_response([{
                "name": property_id.name,
                "id": property_id.id,
                "postcode": property_id.postcode,
                "state": property_id.state
             } for property_id in property_ids], 200)

        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)




