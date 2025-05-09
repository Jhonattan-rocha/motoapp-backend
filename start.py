import os

os.system("hypercorn main:app --bind 0.0.0.0:8000 --workers 4")