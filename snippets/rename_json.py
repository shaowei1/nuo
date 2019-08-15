import json
import codecs

filename = ["./alimama_att_52.json", "./alimama_sent_52.json", ]
destination = "result.json"
input1 = json.load(codecs.open(filename[0], 'r', 'utf-8-sig'))
input2 = json.load(codecs.open(filename[1], 'r', 'utf-8-sig'))

att = dict((i.get("productproid"),
            {"category": i.get("category"), "productproid": i.get("productproid"), "attributes": i.get("attributes"),
             "categories": i.get("categories"), "name": i.get("name")}) for i in input1)

[i.update(att.get(i.get("proid"))) for i in input2]

json.dump(input2, codecs.open(destination, 'w', 'utf-8-sig'))
