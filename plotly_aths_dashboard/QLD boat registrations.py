import urllib


url = 'https://www.data.qld.gov.au/api/3/action/datastore_search?limit=5&resource_id=5a49f720-b0ca-47a8-a19b-24f7fc9493b4&q=title:jones'
fileobj = urllib.urlopen(url)
print(fileobj.read())
