from mongoengine import fields
from PyQt4 import QtGui


class FieldMixin(object):
    def __repr__(self):
        return "{}: name: '{}', value: '{}'".format(
            self.__class__, self.name, self.value)


def create_instance(base, parent, fieldname, obj):
    self = type(base.__name__, (base, FieldMixin), {})(parent=parent)
    self.field = obj._fields[fieldname]
    self.name = fieldname
    self.obj = obj
    self.value = getattr(obj, fieldname)
    return self


class StringFieldWidget(object):
    def __new__(cls, fieldname, obj, parent=None, readonly=None):
        if obj._fields[fieldname].choices:
            self = create_instance(QtGui.QComboBox, parent, fieldname, obj)
            self.addItems(self.field.choices)
            self.setCurrentIndex(self.field.choices.index(self.value))

            def set_value_by_index(i):
                self.value = self.field.choices[i]
                setattr(self.obj, fieldname, self.value)
            self.currentIndexChanged.connect(set_value_by_index)

        else:
            self = create_instance(QtGui.QLineEdit, parent, fieldname, obj)
            self.setText(str(self.value))

            def set_value(*args):
                self.value = self.text()
                setattr(self.obj, fieldname, self.value)
            self.returnPressed.connect(set_value)

        if readonly is not None:
            self.setReadOnly(readonly)

        return self


def ReadOnlyStringFieldWidget(fieldname, obj, parent=None):
    return StringFieldWidget(fieldname, obj, parent, readonly=True)


class DateTimeFieldWidget(object):
    def __new__(cls, fieldname, obj, parent=None):
        self = create_instance(QtGui.QDateTimeEdit, parent, fieldname, obj)
        self.setDateTime(self.value)
        return self

field_to_widget_dict = {
    fields.ObjectIdField: ReadOnlyStringFieldWidget,
    fields.StringField: StringFieldWidget,
    fields.DateTimeField: DateTimeFieldWidget}


def getwidget(field):
    for f, widget in field_to_widget_dict.items():
        if f.__name__ == field.__class__.__name__:
            return widget
    return ReadOnlyStringFieldWidget
