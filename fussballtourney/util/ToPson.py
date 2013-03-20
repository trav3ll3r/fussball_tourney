from Pson import Pson

class ToPson():
    def ToPsonString(self, resource):
        pson = Pson()

        #resource = func(self)

        #pson.setAllowedFieldsString(self.request.get('filter'))

        #self.response.headers = setResponseHeaders()
        #self.response.out.write(pson.encodeModel(resource))

        return pson.encodeModel(resource)

def setResponseHeaders():
    h = {'Content-Type': 'application/json', 'Pragma':'no-cache'}
    return h