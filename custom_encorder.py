from decimal import Decimal
import json

class CustomEncorder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
            
        return json.JSONEncoder.default(self, obj)