# xlr-import-csv-template-plugin

## Introduction: ##
This plugin will allow you to import simple, custom Excel spreadsheets into templates in XL Release.

## CI status ##

[![Build Status][xlr-import-csv-template-plugin-travis-image] ][xlr-import-csv-template-plugin-travis-url]
[![License: MIT][xlr-import-csv-template-plugin-license-image] ][xlr-import-csv-template-plugin-license-url]

[xlr-import-csv-template-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-import-csv-template-plugin.svg?branch=master
[xlr-import-csv-template-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-import-csv-template-plugin
[xlr-import-csv-template-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-import-csv-template-plugin-license-url]: https://opensource.org/licenses/MIT

## Installation requirements ##

- Tested with XL Release 7.2.x and 7.5.x, but should work with lower 7 versions too.

## Installation: ##

Copy the plugin file to the XL Release plugin folder and restart the XL Release server. 

## Usage ##

Although this plugin is very easy adaptable to your own spreadsheet format, it's made to import whatever XL Release export:
![export-template](docs/export-template.png)

You can edit it in Excel, select the entire workbook and copy it to your clipbard
![copy-from-excel](docs/copy-from-excel.png)

Click on the CSV menu item. You can name the new template and paste the fields into the text area.
![csv-import](docs/csv-import.png)

XL Release will give you a link to the imported template.
![csv-imported](docs/csv-imported.png)

As you see, the imported template is not one-to-one, but it's a good 80%.
![imported-template](docs/imported-template.png)

Fields currently supported: see ```field_to_column_index_mapping``` in [CsvParser.py](src/main/resources/csv_import/CsvParser.py).


## Testing ##

Unittests are ran by gradle as part of the lifecyle ```./gradlew test```. This only tests the CsvParser though. UPDATE THE UNITTESTS IF YOU EXPAND THIS PLUGIN!


