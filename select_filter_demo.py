from pyautocad import Autocad, APoint, Q


acad = Autocad()
doc = acad.app.Documents.Add()
model = doc.ModelSpace

# Create some AutocCAD entities
p1 = APoint(0, 0, 0)
p2 = APoint(10, 10, 0)
for i in range(10):
    acad.model.AddLine(p1, p2)
    acad.model.AddCircle(p1, (i + 1) * 10)
    p1.y += 10

for i in range(15):
    model.AddMText(p2, 10, 'Text %s' % i)
    p2.y += 10

# Select demo
#############

# select all circles
print doc.select(type='circle').Count
# select circles with radius greater than 50
print doc.select(type='circle', radius__gt=50).Count
# select circles or multi texts
print doc.select(Q(type='circle') | Q(type='mtext')).Count
# select all objects except Mtext
print doc.select(~Q(type='mtext')).Count
# Patterns search (see Autocad help)
print doc.select(type='mtext', text='Text*').Count
print doc.select(type='mtext', text='Text #').Count


# Filter demo
#############

# Attributes and text operations (startswith, endswith, contains, icontains, re)
print model.filter(ObjectName='AcDbMText', TextString__startswith="Text").count()
# __in operation
print model.filter(ObjectName__in=['AcDbMText', 'AcDbCircle']).count()
# position
print model.filter(InsertionPoint=APoint(10, 10)).count()
# position component
print model.filter(InsertionPoint__x=10).count()
# position component and relational operator (lt, lte, gt, gte)
print model.filter(InsertionPoint__y__gt=20).count()
# extract text length and check if it greater than 5
print model.filter(TextString__len__gt=5).count()
# Attribute range
print model.filter(Radius__range=(20, 50)).count()
# distance functions (equal)
print model.filter(InsertionPoint__distance=(APoint(10, 10), 10)).count()
# distance functions with relation (lt, gt, lte, gte)
# note single underscore before gt
print model.filter(InsertionPoint__distance_gt=(APoint(0, 0), 30)).count()

# ordering by multiple conditions
for mtext in model.filter(ObjectName='AcDbMText').\
             best_interface().order_by('-TextString__len', '-InsertionPoint__y'):
    print mtext.TextString



# DELETEME
doc.Close(False)