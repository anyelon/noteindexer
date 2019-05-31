from docx import *
from pathlib import Path
from elasticsearch import Elasticsearch


def main():
    es = Elasticsearch()
    es.indices.create(index='notes',body="""
             {
                   "settings":{
                      "analysis":{
                         "filter":{
                            "stemmer":{
                               "type":"stemmer",
                               "language":"english"
                            },
                            "stopwords":{
                               "type":"stop",
                               "stopwords":[
                                  "_english_"
                               ]
                            }
                         },
                         "analyzer":{
                            "custom_analyzer":{
                               "filter":[
                                  "stopwords",
                                  "lowercase",
                                  "stemmer"
                               ],
                               "type":"custom",
                               "tokenizer":"standard"
                            }
                         }
                      }
                   },
                   "mappings":{
                         "properties":{
                            "name":{
                               "type":"text",
                               "analyzer":"custom_analyzer",
                               "search_analyzer":"custom_analyzer"
                            },
                            "content":{
                               "type":"text",
                               "analyzer":"custom_analyzer",
                               "search_analyzer":"custom_analyzer"
                            }
                         }
                      }
                }
     """,ignore=400)
    result = list(Path(".").rglob("*.[dD][oO][cC][xX]"))

    for filename in result:
        document = Document(filename)
        docText = '\n\n'.join([paragraph.text for paragraph in document.paragraphs])
        content = str(docText).replace("\n","").replace("\"",'\'')
        body = """
        {
            "name": \"""" + filename.name + """\",
            "content":\"""" + content + """\"
        }
        """
        es.index(index='notes', body=body)


if __name__ == '__main__':
    main()
