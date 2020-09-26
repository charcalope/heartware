# Development Guidelines

### General Guidelines

- Document/comment *whenever possible* - will make keeping code working and updated much easier, especially with multiple people working with the repo
- Separate blocks of dissimilar code with indents, comment blocks to describe their use

### Web Design

- Always use templates (as opposed to static HTML files) and place them under templates/, or Flask will not detect them
- Make sure to create a route in Flask to any pages that are mostly finalized

### Web Server 

- Abstract when possible - main app.py will end up containing a lot of web-server logic/routes, and any code in there beyond initializing services and registering jobs will add to the clutter

### Board Representation

- When adding new python packages, use the `install_pkg` scripts so the integrity of the requirements.txt file is kept and the packages are installed under the virtual env. 

### Board Firmware

- Placeholder
