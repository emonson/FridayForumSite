## Visualization Friday Forum schedule site code

These are the files that support the schedule page for the [Visualization Friday Forum][vff] 
at [Duke University][duke].

The data for the past and upcoming talks is kept in a [Google Spreadsheet][data] that
has a separate tab for each semester. In the past, besides adding a new tab to the spreadsheet, 
I had to create a new page every semester and change some header and footer info in old ones.
Now, the schedule page itself is a single page application that draws from that data and automatically
deals slightly differently with the current page vs past or future semesters. 

For convenience of programming, I make a separate Excel spreadsheet, `SiteNames.xlsx`, which specifies the tab
names, and holds some other metadata necessary for creating the `sitemap.xml` file which
Google uses for indexing since there are not individual page files for each semester's schedule.

### New semester

When you want to add a new semster on to the schedule:

1. Add a new tab to the Google spreadsheet with the name of the semester in the format `(Fall|Spring)_YYYY`.
1. Add a new row to the `SiteNames.xlsx` file with the new tab name in the Semester column
1. Update which semesters are current, past or future.
1. Update dates when Google should think the pages were last modified. None required for current or future.
1. I've been using 0.6 priority for current, 0.3 for one semster past, 0.1 for two semesters past
and 0.05 for further past. No priority value is entered for future semesters.
1. Run the `excel2json_sheetnames_sitemap.py` script to generate both the JSON file the site
Javascript will use, plus the `sitemap.xml` file that Google will use for indexing the site.


[vff]: http://vis.duke.edu/FridayForum/ "Visualization Friday Forum"
[duke]: http://www.duke.edu/ "Duke University"
[data]: https://docs.google.com/spreadsheet/pub?key=0AgpG-BX4vPChdGdQdGllSEc1eDlTMjl5NUZjWVdnTHc&output=html "Data sheet"

