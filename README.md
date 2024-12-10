The Pegasus program is designed for advanced computational analysis in astronomical contexts. 
Below is a detailed explanation of the folder structure and functionalities of the program, 
along with a list of every script and its function.

**Folder Structure and Functionalities**
data_tables_reader: Contains scripts for reading and processing data tables, specifically from web sources.

website_1: Contains scripts for initial data reading and conversion (abandoned in favor of version 2).

website_data_reader_v1.py: Reads positional data from a specified website and calculates velocities.
website_2: Contains updated scripts for reading and processing data tables from NASA's Horizon System.

website_data_reader_v2.py: Reads multiple files with initial positions and velocities, converting units to SI
and generating a formatted initial conditions file.

Eclipse_test: Contains data files used for testing eclipse predictions.

horizons_results (0).txt and horizons_results (2).txt: Example data files with positional and velocity information.

**Script Details**

main.py: Runs simulations based on initial conditions and parameters, displaying results and saving data.

main(): Reads initial conditions and parameters, advances the simulation state, and saves results.
astros.py: Defines classes and methods for representing astronomical objects and their interactions.

Astro: Represents an astronomical object with properties like position, velocity, and mass.
AstroList: Manages a collection of astronomical objects, handling interactions and state updates.
eclipse_search.py: Implements functions to study and predict solar and lunar eclipses.

eclipse_check(): Checks if the configuration of astronomical bodies indicates an eclipse.
search_eclipse(): Planned function for efficient eclipse search using position lists.
moon_phase.py: Simulates and names moon phases based on the positions of the Sun, Earth, and Moon.

get_moon_phase(): Calculates and displays the moon phase, saving a visual representation.
data_tables_reader/website_1/website_data_reader_v1.py:

rewrite_table_web(): Writes a new table with formatted data.
create_data_file_from_website(): Extracts data from two files and generates a new data file.
data_tables_reader/website_2/website_data_reader_v2.py:

read_files(): Reads initial position and velocity files, converts units, and generates a formatted initial conditions file.
