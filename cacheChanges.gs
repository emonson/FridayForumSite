// Function to cache spreadsheet to s3 with table-service server
// Call on-demand or however you like
function cacheChanges() {
   var key = SpreadsheetApp.getActiveSpreadsheet().getId();
   var sheet_name = SpreadsheetApp.getActiveSheet().getSheetName();
  
   var payload =
   {
     "key" : key,
     "sheet_name" : sheet_name
   };
  
   var options =
   {
     "method" : "post",
     "payload" : payload
   };
  
   UrlFetchApp.fetch("http://whitney.trinity.duke.edu/cgi-bin/table-service/es_index_server.py", options);
  
}

