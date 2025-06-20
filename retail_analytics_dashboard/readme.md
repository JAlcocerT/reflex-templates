Run the reflex webapp:

```sh
cd ./retail_analytics_dashboard
reflex run
reflex run --backend-port 8001 --frontend-port 3001
```

```sh
sudo apt-get install python3-virtualenv

#python -m venv solvingerror_venv #create the venv
python3 -m venv solvingerror_venv #create the venv

#solvingerror_venv\Scripts\activate #activate venv (windows)
source solvingerror_venv/bin/activate #(linux)

#pip install reflex==0.7.0
pip install -r requirements.txt #all at once
#pip freeze | grep langchain

#pip show beautifulsoup4
pip list
pip freeze > requirements-output.txt #generate a txt with the ones you have!
```