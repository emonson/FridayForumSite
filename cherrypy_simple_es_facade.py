import cherrypy
from elasticsearch import Elasticsearch

class SimpleEsServer(object):
    
    def __init__(self):
        
        self.es = Elasticsearch()
        
    @cherrypy.expose
    def index(self):
        
        return str(self.es.ping())
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def search(self):
        
        return self.es.search(index="fashion_test", body={"query": {"match_all": {}}})

if __name__ == '__main__':
    
    cherrypy.quickstart(SimpleEsServer())