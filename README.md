## Usage
```pip3 install -r requirements.txt```
- [Limelighter](https://github.com/Tylous/Limelighter) is required for testsigs command (Within PATH) 

```
> python3 .\certdisco.py -h

    __    ___  ____   ______  ___    ____  _____    __   ___
   /  ]  /  _]|    \ |      ||   \  |    |/ ___/   /  ] /   \
  /  /  /  [_ |  D  )|      ||    \  |  |(   \_   /  / |     |
 /  /  |    _]|    / |_|  |_||  D  | |  | \__  | /  /  |  O  |
/   \_ |   [_ |    \   |  |  |     | |  | /  \ |/   \_ |     |
\     ||     ||  .  \  |  |  |     | |  | \    |\     ||     |
 \____||_____||__|\_|  |__|  |_____||____| \___| \____| \___/

                 @ed
          Code Signing Certificate Discovery Tool

usage: certdisco.py [-h] {import,view,vt,testsigs} ...

Process and view certificates.

positional arguments:
  {import,view,vt,testsigs}
    import              Process new certificates
    view                View stored certificates
    vt                  Fetch files from VirusTotal
    testsigs            Run limelighter with certificates

```

#### Pull .p12 and .pfx files from VirusTotal (Last 75 days)
```
python3 certdisco.py vt --api '<apikey>' -q 100 -o vt-output
```

#### Attempt to Crack and Store Certificates from DIR
```
python3 certdisco.py import -i vt-output
```

#### View/Export Database
```
python3 certdisco.py view
python3 certdisco.py view --export
```
#### Sign a test EXE with every recovered certificate in DB
This does require limelighter to be installed and in your PATH
```
python3 certdisco.py testsigs --certlocation vt-output -o export
*File export.zip will be generated* 
```

I just unzip on windows and use signtool.exe to check for validity
```signtool verify /pa /v *.exe```
