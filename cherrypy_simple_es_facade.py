import cherrypy
from collections import defaultdict
from elasticsearch import Elasticsearch

from ES_FF_Reindex import es_ff_reindex

# Create arbitrarily nested default dictionaries
# http://stackoverflow.com/questions/19189274/defaultdict-of-defaultdict-nested
def rec_dd():
    return defaultdict(rec_dd)


class SimpleEsServer(object):
    
    def __init__(self):
        
        self.es = Elasticsearch()
        
    @cherrypy.expose
    def index(self):
        
        return str(self.es.ping())
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def search(self, q=''):
        
        search_fields = ['speaker','title','affiliation','abstract']
        exclude_return = ['gs_key','gs_sheet_id','gs_link']
        
        body = rec_dd()
        body['query']['multi_match']['query'] = q
        body['query']['multi_match']['fields'] = ['speaker','title','affiliation','abstract']
        
        res = self.es.search(index="friday_forum_test", 
                                doc_type='talks', 
                                body=body, 
                                size=20, 
                                _source_exclude=exclude_return)
        
        # Don't return score, number of hits, time took, etc.
        return [hit['_source'] for hit in res['hits']['hits']]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def semester(self, s=None):
        
        if s is not None:
            exclude_return = ['gs_key','gs_sheet_id','gs_link']
            
            # Right now the sheet_name field is being analyzed with "standard", which
            # lowercases but does not split on underscore, so since filters are not
            # run through the analyzer, need to make sure I lowercase before query
            body = rec_dd()
            body['query']['filtered']['filter']['term']['sheet_name'] = s.lower()
        
            res = self.es.search(index="friday_forum_test", 
                                    doc_type='talks', 
                                    body=body, 
                                    size=20, 
                                    _source_exclude=exclude_return,
                                    sort='date:asc')
        
            # Don't return score, number of hits, time took, etc.
            return [hit['_source'] for hit in res['hits']['hits']]

    @cherrypy.expose
    def reindex_sheet(self, modified_sheet=None):
        
        if modified_sheet is not None:
            
            es_ff_reindex(modified_sheet=modified_sheet, RECREATE=False, es=self.es)
            
        return

if __name__ == '__main__':

    cherrypy.config.update({
            'server.socket_port': 9102, 
            # 'server.socket_host': '10.190.55.12'
            'server.socket_host': 'localhost'
            })
            
    cherrypy.quickstart(SimpleEsServer())