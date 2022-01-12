# Cognitive Consilience
Attempt to resurrect a dead fusion-tables dependent web-app

**Source materials:** 
1. Adobe illustrator diagrams, designed in a way that allow for export 
	- Export to zoomify tiles (base capability of illustrator)
	- Export to raster PSB file (base capability of illustrator)
	- Export to SVG (base capability of Photoshop)
2. Python script to consolidate tiles and add a black border to them (not entirely needed)
3. Python script to extract reference ID and location from SVG
4. Python script to extract reference ID from endnote XML file and populate from pubmed

## How it works (V1)

### Generation of materials
- The references are maintained in a endnote or other computer-readable database
	- Each reference is tagged with an ID (numeric)
- References are added to the illustrator file in a separate layer
- The illustrator file is exported to a SVG 
	- A script extracts the positions from the SVG in absolute coordinates and generates a JSON file of the references
	- A script merges the positions with the reference information and fills in details from pubmed via external query
	- A script generates a sqlite database for the iOS app
	- A script converts the data to a table and uploads it to create a Google Fusion table (now dead)
- The Illustrator file is exported to a PSB file for rasterization in photoshop
	- Each layer is exported as a tiled pyramid in zoomify format

### Visualization of materials
- A tiled image viewer is used to display each rasterized view of the cortical layers
- Web viewer functionality
	- A javascript UI (ancient jquery) was used to toggle different layers
	- A javascript UI to display a custom google maps layer (tiled pyramid image tiles, served statically)
		- We project the tiles into a geographic coordinate system
	- A javascript query to the Google maps / fusion table layer to display features on the map
		- We project the locations of the references into a geographic coordinate system
	- A javascript query to filter the features on a map based on a text search, or a date search
- Services
	- Static hosting of html, javascript, and tiled images
	- Fusion table providing an endpoint to display references in a geospatial form

## How it could work (V2?)
- Convert sqlite database into either browser-based client DB / store or endpoint-based (graphql or REST-like), potentially use geojson for feature encoding
- Replace Google maps and geospatial referencing with modern webgl-based viewer (deck.gl or openlayers) 
- Replace tiled image layers with vector image rendering
- Add dynamic references and relationships by layer / circuit / etc

