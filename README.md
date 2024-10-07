# Product-Recommender

Set up Apache Solr
1. Download Solr 9.x from https://solr.apache.org/downloads.html and decompress 
2. In the solr-9.x.0 folder run 
```
bin/solr start -c
```
3. Open http://localhost:8983/solr/ and create `venue_menu` and `catalogues` collections with the default schema
4. In the root directory, run
```
pipenv run python3 index_all.sh
```

Set up frontend 
