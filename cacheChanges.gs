// For CGI server onChange notifications (from table-service)
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

/* 
https://productforums.google.com/forum/#!topic/docs/s28qb3Cw_xw
*/

function SheetName(input) {
  var idx = parseInt(input);
  var doc = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = doc.getSheets();
  
  return (idx >= 0 && idx < sheets.length) ? sheets[idx].getName() : '';
}

// For CGI server onChange notifications (from table-service)
// Function to cache spreadsheet to s3 with table-service server
// Call on-demand or however you like
function cacheChangesAllGET() {
  var origin_key = SpreadsheetApp.getActiveSpreadsheet().getId();
  var modified_sheet_name = SpreadsheetApp.getActiveSheet().getSheetName();
  
  var url_base = "http://10.190.55.12:9102/reindex_all";
  
  var server_url = url_base + "?key=" + origin_key;
  
  UrlFetchApp.fetch(server_url);
}

// For CGI server onChange notifications (from table-service)
// Function to cache spreadsheet to s3 with table-service server
// Call on-demand or however you like
function cacheChangesOneGET() {
  var origin_key = SpreadsheetApp.getActiveSpreadsheet().getId();
  var modified_sheet_name = SpreadsheetApp.getActiveSheet().getSheetName();
  
  var url_base = "http://10.190.55.12:9102/reindex_sheet";
  
  var server_url = url_base + "?key=" + origin_key + "&modified_sheet_name=" + modified_sheet_name;
  
  UrlFetchApp.fetch(server_url);
}

/**
 * Retrieves all the rows in the active spreadsheet that contain data and logs the
 * values for each row.
 * For more information on using the Spreadsheet API, see
 * https://developers.google.com/apps-script/service_spreadsheet
 */
function readRows() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var rows = sheet.getDataRange();
  var numRows = rows.getNumRows();
  var values = rows.getValues();

  for (var i = 0; i <= numRows - 1; i++) {
    var row = values[i];
    Logger.log(row);
  }
};

/**
 * Adds a custom menu to the active spreadsheet, containing a single menu item
 * for invoking the readRows() function specified above.
 * The onOpen() function, when defined, is automatically invoked whenever the
 * spreadsheet is opened.
 * For more information on using the Spreadsheet API, see
 * https://developers.google.com/apps-script/service_spreadsheet
 */
function onOpen() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var entries = [{name : "Read Data", functionName : "readRows"},
                 {name : "ES Reindex All", functionName : "cacheChangesAllGET"}];
  spreadsheet.addMenu("Script Center Menu", entries);
};
