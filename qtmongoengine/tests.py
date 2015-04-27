import os
from mongoengine import fields, Document
import mongoengine
import fieldwidgets
from fieldwidgets import StringFieldWidget
from PyQt4 import QtGui
import subprocess
import datetime
subprocess.Popen('C:/Programme/MongoDB/Server/3.0/bin/mongod.exe --dbpath d:/db')

app = QtGui.QApplication.instance()
if not app:
    app = QtGui.QApplication([])

# f = fields.StringField(choices=list('abcdefg'))
# s = StringFieldWidget(f)
# s.show()
#
# f1 = fields.StringField()
# s1 = StringFieldWidget(f1)
# s1.show()
#
mongoengine.connect()


class Test(Document):
    name = fields.StringField()
    sex = fields.StringField(choices=('Male', 'Female', 'Other'))
    date = fields.DateTimeField(default=datetime.datetime.now())

Test(name='Angela', sex='Male').save()
Test(name='Wurst', sex='Other').save()

widgets = []
for obj in Test.objects:
    for fieldname in Test._fields_ordered:

        widgets.append(StringFieldWidget(
            fieldname,
            obj))


class CollectionTableWidget(QtGui.QTableWidget):
    def __init__(self, collection=None, parent=None):
        super(self.__class__, self).__init__(parent=parent)
        self.collection = collection
        self.setRowCount(self.collection.objects.count())
        self.setColumnCount(len(self.collection._fields))
        self.fields = collection._fields_ordered
        self.set_items(collection)

        def on_cell_changed(irow, icol):
            obj = self.collection.objects[irow]
            print(irow, icol)

        self.cellChanged.connect(on_cell_changed)

    def set_items(self, collection=None):
        if collection is None:
            collection = self.collection
        else:
            self.collection = collection

        self.setHorizontalHeaderLabels(self.fields)
        for icol, col in enumerate(self.fields):
            field = collection._fields[col]
            Widget = fieldwidgets.getwidget(field)
            for irow, obj in enumerate(collection.objects):
                widget = Widget(col, obj, parent=self)
                self.setCellWidget(irow, icol, widget)


c = CollectionTableWidget(Test)
