# Define Python interpreter
PYTHON = python3

# Define test file
TEST_FILE = test_backEndShopLyft.py

# Define backend and frontend scripts
BACKEND_FILE = backEndShopLyft.py
FRONTEND_FILE = frontEndShopLyft.py

# Default target
all: test

# Run unit tests
test:
	$(PYTHON) -m unittest $(TEST_FILE)

# Run backend
run_backend:
	$(PYTHON) $(BACKEND_FILE)

# Run frontend
run_frontend:
	$(PYTHON) $(FRONTEND_FILE)

# Clean up cache files
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete