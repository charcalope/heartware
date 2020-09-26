# Usage

### Initial Setup

**Note:** You should have Python3 installed on your computer and accessible via command-line. If not, go and download Python3 from [the Python downloads page](https://www.python.org/downloads/) first.

First, download the repository as needed

```bash
cd <Path to install location>
git clone https://github.com/charcalope/heartware
cd heartware
```

Then, run the start script specific to your OS

##### Linux/MacOS

```
./start_server.sh
```

##### Windows

```
> start_server.bat
```

This script should detect if the virtual environment is set up or not (it shouldn't be on first-time setup), set it up, enable it, and install all requirements (frozen to `requirements.txt`)

### Development

Assuming you have a command line open in the respective directory, just run the start_server script specific to your OS and all should be well.

##### Linux/MacOS

```bash
./start_server.sh
```

##### Windows

```
> start_server.bat
```

Then, Flask will return the IP and the port that it is bound to - simply navigate to that IP and port in your browser and the website should show up.

### Production

TBD!