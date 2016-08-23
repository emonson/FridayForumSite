import os, base64, re, logging
from elasticsearch import Elasticsearch
import urllib2
import json
import dateutil.parser
import warnings

def es_ff_reindex(modified_sheet_name='_', RECREATE=False, es=None):
    
    if es is not None:
    
        # Now also make a connection to Elasticsearch
        es_index_name = 'friday_forum_test'
        es_doc_type = 'talks'
        key =  '1x_pPSVaxifb1EpqqKeQfUYyTkuVt0_7oYwqHcLhHDME'
        
        doc_mapping = { "properties": {
            "abstract": { "analyzer": "english", "type": "string" },
            "affiliation": { "analyzer": "standard", "type": "string" },
            "speaker": { "analyzer": "standard", "type": "string" },
            "sheet_name": { "analyzer": "standard", "type": "string" },
            "gs_link": { "index": "no", "type": "string" },
            "gs_key": { "index": "no", "type": "string" },
            "gs_sheet_id": { "index": "no", "type": "string" },
            "video": { "index": "no", "type": "string" },
            "slides": { "index": "no", "type": "string" },
            "livestream": { "index": "no", "type": "string" }
            # "date": { "format": "date", "type": "dateOptionalTime" }
          }
        }

        # DANGER -- Delete index!!
        if RECREATE and es.indices.exists( index = es_index_name ):
            es.indices.delete(index=es_index_name)

        # Create the index
        if not es.indices.exists( index = es_index_name ):
            es.indices.create( index = es_index_name, body={ "number_of_shards": 1 } )
            es.indices.put_mapping(index=es_index_name, doc_type=es_doc_type, body=doc_mapping)

        sheets_json_url = "https://spreadsheets.google.com/feeds/worksheets/"+key+"/public/basic?alt=json"
        sheets_json = urllib2.urlopen(sheets_json_url).read()
        sheets_dict = json.loads(sheets_json)

        for entry in sheets_dict['feed']['entry']:
            sheet_name = entry['title']['$t']
            sheet_id = urllib2.urlparse.urlparse(entry['id']['$t']).path.split('/')[-1]
    
            # If recreating whole index, need to loop through all sheets, otherwise only modified one for performance.
            # Unfortunately, google doesn't let you get more granular than the sheet level to say where mods happened.
            if sheet_name == modified_sheet_name or RECREATE:
    
                sheet_json_url = "https://spreadsheets.google.com/feeds/list/"+key+"/"+sheet_id+"/public/values?alt=json"
                sheet_json = urllib2.urlopen(sheet_json_url).read()
                sheet_dict = json.loads(sheet_json)
        
                for row in sheet_dict['feed']['entry']:
                    doc = {}
                    doc_id = None
            
                    doc['gs_link'] = row['id']['$t']
                    doc['sheet_name'] = sheet_name
                    doc['gs_key'] = key
                    doc['gs_sheet_id'] = sheet_id
            
                    column_names = [k for k in row.keys() if k.startswith('gsx$')]
                    for col_name in column_names:
                        real_name = col_name[4:].lower().replace(' ','_')
                        cell_value = row[col_name]['$t']
                        # Don't want to put field in doc if empty cell
                        if cell_value:
                            # Using date as unique ID for talk, but changing to YYYY-MM-DD format
                            if real_name == 'date':
                                date_str = cell_value
                                dd = dateutil.parser.parse(date_str)
                                doc_id = dd.date().isoformat()
                                # and serializing date as datetime object for real time object in ES
                                doc['date'] = dd
                            else:
                                doc[real_name] = cell_value

                    # store talk in ES
                    res = es.index(index=es_index_name, doc_type=es_doc_type, id=doc_id, body=doc)
                    
if __name__ == '__main__':
    
#     es = Elasticsearch()
#     es_ff_reindex(RECREATE=True, es=es)
    
    # Log transport details (optional):
    logging.basicConfig(level=logging.INFO)

    # Parse the auth and host from env:
    bonsai = os.environ['BONSAI_URL']
    auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
    host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

    # Connect to cluster over SSL using auth for best security:
    es_header = [{
      'host': host,
      'port': 443,
      'use_ssl': True,
      'http_auth': (auth[0],auth[1])
    }]

    # Instantiate the new Elasticsearch connection:
    # Getting urllib3 warnings about InsecureRequestWarning - obscuring other output
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        es = Elasticsearch(es_header)
        es_ff_reindex(RECREATE=True, es=es)
