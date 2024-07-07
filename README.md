## Usage
```pip3 install -r requirements.txt```
- john the ripper is required (pfx2john/john)
- [Limelighter](https://github.com/Tylous/Limelighter) is required for testsigs command (Within PATH)
- Hardcoded wordlist path /usr/share/wordlists/rockyou.txt (modify this [line](https://github.com/0xflagplz/CodeSigningScrape/blob/d96e31de5d2c10bc033173a397490b12ad61c842/src/process.py#L32) to change)
- Hardcoded john format is --format=pfx (not pfx-opencl)

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


Notes
- Based of this [article](https://tij.me/blog/finding-and-utilising-leaked-code-signing-certificates/) by Tijme Gommers 
- [Query](https://github.com/0xflagplz/CodeSigningScrape/blob/1d2125765b76de82683d67a6a4bad46b35b42c89/src/virustotal.py#L55): content:{02 01 03 30}@4 NOT tag:msi AND NOT tag:peexe AND ls:75d+
- Modify [this](https://github.com/0xflagplz/CodeSigningScrape/blob/1d2125765b76de82683d67a6a4bad46b35b42c89/src/virustotal.py#L63) line to include more/less restrictions on downloaded file extensions
