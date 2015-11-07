from cmislib import CmisClient, Repository, Folder

client = CmisClient('http://cmis.alfresco.com/cmisatom', 'admin', 'admin')

repo = client.defaultRepository

print repo.id

info = repo.info
for k,v in info.items():
    print "%s:%s" % (k,v)


#root = repo.rootFolder
#someFolder = root.createFolder('testharicmslibpython5')
#print someFolder.id

someFolder = repo.getObjectByPath('/testharicmslibpython5')

someFile = open('/Users/harikolasani/Desktop/test.txt', 'r')
someDoc = someFolder.createDocument('Test Hari 3 Document', contentFile=someFile)
props = someDoc.properties
for k,v in props.items():
    print '%s:%s' % (k,v)

results = repo.query("select * from cmis:document where cmis:name LIKE '%Hari%'")
for result in results:
    print result.name

someDoc = repo.getObject('workspace://SpacesStore/40c5708d-6af9-43b1-bbd0-261062ec1ff0')
print someDoc.name
someDoc.getContentStream()
children= someFolder.getChildren()
for child in children:
    print child.name

o = open('/Users/harikolasani/Desktop/tmp.txt', 'wb')
result = someDoc.getContentStream()
o.write(result.read())
result.close()
o.close()