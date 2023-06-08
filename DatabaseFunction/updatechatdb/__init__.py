import azure.functions as func
import json

def main(req: func.HttpRequest, item: func.Out[func.SqlRow]) -> func.HttpResponse:
    
    body = json.loads(req.get_body())
    row = func.SqlRow.from_dict(body)
    name = req.params.get('name')
    item.set(row)

    return func.HttpResponse(
        body=req.get_body(),
        status_code=201,
        mimetype="application/json"
    )