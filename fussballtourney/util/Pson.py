import json, inspect
import collections
import datetime
from google.appengine.ext import db
from RestApiResponse import RestApiResponse

###
# JSON Serialiser for python (PSON)... yep, name stolen from GSON
#
from DateUtil import formatFullDatetime

class Pson:
    # Specifies the field names that are allowed to be serialised.
    # Defaults to all (i.e. '*.*')
    _allowedFields = ['*.*']

    # Specifies the field names that are NOT allowed to be serialised.
    # Defaults to any password field
    _disallowedFields = ['*.password']

    def setAllowedFieldsString(self, str):
        if not str or str == '':
            return

        self._allowedFields = []

        for chunk in str.split('~'):
            rightBracketRemoved = chunk.split(')')[0]

            className = rightBracketRemoved.split('(')[0]
            fields = rightBracketRemoved.split('(')[1]

            for field in fields.split(','):
                self._allowedFields.append('%s.%s' % (className, field))

    def setAllowedFields(self, allowedFields):
        self._allowedFields = allowedFields

    def encodeModelList(self, l):
        return json.dumps(self._createJsonList(l, []))

    def encodeModel(self, m):
        return json.dumps(self._createJsonObject(m, []))

    def _createJsonList(self, l, done):
        jsonList = []

        for el in l:
            jsonList.append(self._createJsonObject(el, done[:]))

        return jsonList

    def _createJsonObject(self, m, done):
        jsonObject = {}

        # If the Model is saved then update the 'id' field to contain the models proper id
        if hasattr(m, 'is_saved'):
            jsonObject = {'id': None}
            if m and m.is_saved():
                key = getattr(m, 'key')()

                jsonObject['id'] = key.id()
                done.append(key)

            for f, attr in self._getJsonFields(m, done).iteritems():
                if isinstance(attr, (int, long, float, bool, dict, basestring)):
                    jsonObject[f] = attr
                elif isinstance(attr, datetime.date):
                    jsonObject[f] = formatFullDatetime(attr)
                elif isinstance(attr, datetime.datetime):
                    jsonObject[f] = 'datetime' #formatFullDatetime(attr)
                elif isinstance(attr, db.GeoPt): # Added for no real reason
                    jsonObject[f] = {'lat': attr.lat, 'lon': attr.lon}
                elif isinstance(attr, collections.Iterable):
                    jsonObject[f] = self._createJsonList(attr, done)
                else:
                    jsonObject[f] = self._createJsonObject(attr, done)
        else:
            if isinstance(m, RestApiResponse):
                jsonObject['httpStatus'] = m._httpStatus
                jsonObject['urn']        = m._urn
                jsonObject['count']      = m._count
                jsonObject['items']      = self._createJsonList(m._items, done[:])
            else:
                # This case will trigger if a list of primitive types are serialised
                # in which case, 'm' will be one of the primitive values, so just return it
                return m

        return jsonObject

    def _getJsonFields(self, model, done):
        def isPublicAttribute(name, value):
            return not (name.startswith('_') or inspect.ismethod(value) or inspect.isfunction(value))

        def isReverseReference(name):
            return name.endswith('_set')

        def isProcessed(done, value):
            if hasattr(value, 'key'):
                return getattr(value, 'key')() in done
            else:
                return False

        def isFieldAllowed(model, fieldName):
            className = type(model).__name__

            # First check for disallowed fields
            for disallowedField in self._disallowedFields:
                disallowedClassName = disallowedField.split('.')[0]
                disallowedFieldName = disallowedField.split('.')[1]

                if (className == disallowedClassName or disallowedClassName == '*') and (fieldName == disallowedFieldName or disallowedFieldName == '*'):
                    return False

            # Then check for allowed ones
            for allowedField in self._allowedFields:
                allowedClassName = allowedField.split('.')[0]
                allowedFieldName = allowedField.split('.')[1]

                if (className == allowedClassName or allowedClassName == '*') and (fieldName == allowedFieldName or allowedFieldName == '*'):
                    return True

            return False

        fields = {}
        eligibleFields = dict(inspect.getmembers(model))

        # If the model has a dynamic properties attr, then add them to the existing eligible fields
        # Note: Dynamic properties with conflicting keys will be ignored
        if hasattr(model, '_dynamic_properties'):
            dynamicProps = model._dynamic_properties
            dynamicProps.update(eligibleFields)
            eligibleFields = dynamicProps

        for name, value in eligibleFields.iteritems():
            if isFieldAllowed(model, name):
                if isPublicAttribute(name, value):
                    if not isReverseReference(name):
                        if not isProcessed(done, value):
                            fields[name] = value

        return fields

    @staticmethod
    def basicDecodeToModel(jsonStr, Model):
        jsonDict = json.loads(jsonStr)

        model = Model(**jsonDict)

        return model