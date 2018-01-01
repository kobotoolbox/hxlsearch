### Example installation on Linux

Python 3 is not necessary but was used in this example to avoid SNI warnings
when making HTTPS requests

```
$ virtualenv --python=python3 venv
Running virtualenv with interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in venv/bin/python3
Also creating executable in venv/bin/python
Installing setuptools, pip...done.
$ source venv/bin/activate
(venv)$ pip install requests
Downloading/unpacking requests
  Downloading requests-2.18.4-py2.py3-none-any.whl (88kB): 88kB downloaded
Downloading/unpacking chardet>=3.0.2,<3.1.0 (from requests)
  Downloading chardet-3.0.4-py2.py3-none-any.whl (133kB): 133kB downloaded
Downloading/unpacking certifi>=2017.4.17 (from requests)
  Downloading certifi-2017.11.5-py2.py3-none-any.whl (330kB): 330kB downloaded
Downloading/unpacking idna>=2.5,<2.7 (from requests)
  Downloading idna-2.6-py2.py3-none-any.whl (56kB): 56kB downloaded
Downloading/unpacking urllib3>=1.21.1,<1.23 (from requests)
  Downloading urllib3-1.22-py2.py3-none-any.whl (132kB): 132kB downloaded
Installing collected packages: requests, chardet, certifi, idna, urllib3
Successfully installed requests chardet certifi idna urllib3
Cleaning up...
```

### First run within the same virtualenv

```
(venv)$ python hxlsearch.py '#question3+attr4'
INFO:root:Your query, "#question3+attr4", matches the following question names:
INFO:root:	Question_3_Name
INFO:root:******* BEGIN JSON SUBMISSION OUTPUT *******
[
  {
    "Question_3_Name": "1",
    "_id": 3281008
  },
  {
    "Question_3_Name": "2",
    "_id": 3281009
  },
  {
    "Question_3_Name": "3",
    "_id": 3281010
  }
]
```
