build_local_app:
	uvicorn main:app --reload
unittests:
	 python -m pytest tests/ -v
