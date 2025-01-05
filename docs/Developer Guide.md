# Developer Guide
## For frontend developers:
### First time setting up the environment
> Go to the project
```bash
cd U-BirdEat_Backend
```
> Create a virtual environment backend-env
```bash
python -m venv backend-env 
```
> Activate the virtual environment backend-env
```bash
source ./backend-env/bin/activate
```
> Install the required packages
```bash
pip install -r requirements.txt
```
> Set up the environment variable (put the OpenAI API key in the environment variable):
You can get the API key from the OpenAI platform. For detailed steps, please refer to the [official tutorial of OpenAI](https://platform.openai.com/docs/quickstart?context=python)

### Run the server
> Activate the virtual environment backend-env
```bash
source ./backend-env/bin/activate
```

### If there are missing packages
>安裝所需的套件
```bash
pip install -r requirements.txt
```

## For backend developers:
### First time setting up the environment
> Go to the project
```bash
cd U-BirdEat_Backend
```
> Create a virtual environment backend-env
```bash
python -m venv backend-env 
```
> Activate the virtual environment backend-env
```bash
source ./backend-env/bin/activate
```
> Install the required packages
```bash
pip install -r requirements.txt
```

### Update requirements.txt
> Go to the project
```bash
cd U-BirdEat_Backend
```
> Update requirements.txt
```bash
pip freeze > requirements.txt
```