# Dump Flask Project

---

## Usage

### Step 1: Git clone the repo

```
git clone https://github.com/brianyaucy/dump-flask-project
```

### Step 2: Create virtual environment

```
cd dump-flask-project && python3 -m venv .
source ./bin/activate
pip3 install -r requirements.txt
```

### Step 3: Run the application

By default the application will listen on **tcp/8000**:

```
python3 app.py
```

---

## Functions

- Security
  - [x] Login
  - [x] Password Complexity 
  - [x] 2FA Authentication
  - [ ] Email verification
  - [ ] Logging wrapper
- Function
  - [x] Post
  - [x] Like
  - [x] Timeline Generator
  - [ ] Bulk check domains & visualization
  - [ ] Bulk check IPs & visualization 