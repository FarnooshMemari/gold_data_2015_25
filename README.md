# IDS706_python_template
Data Engineering Duke University

This repository provides a simple Python template for Data Engineering coursework at Duke University (IDS 706). It includes basic Python functions, unit tests, and a development environment setup using Dev Containers.

## Features
- Simple Python functions in [`hello.py`](hello.py)  
- Unit tests in [`test_hello.py`](test_hello.py) using `pytest`  
- Code formatting with `black`  
- Linting with `flake8`  
- Test coverage with `pytest-cov`  
- Dev Container configuration for reproducible environments  

## Setup
1. **Clone the repository:**
   git clone <repo-url>
   cd IDS706_python_template

2. **Open in VS Code:**  
   Open the folder in VS Code and reopen in the Dev Container when prompted.

3. **Install dependencies:**
   make install

## Usage
- **Format code:**  
   make format

- **Lint code:**  
   make lint

- **Run tests:**  
   make test

- **Clean build artifacts:**  
   make clean

- **Run all steps:**  
   make all

### Example: Running the Python functions
You can run the included functions directly from the command line:

   python -c "from hello import say_hello, add; print(say_hello('Annie')); print(add(2,3))"

Expected output:

   Hello, Annie, welcome to Data Engineering Systems (IDS 706)!
   5