from setuptools import setup, find_packages

"""
Creates euro_cert_api as package
"""

requirements = """
annotated-types==0.7.0
anyio==4.10.0
beanie==2.0.0
bcrypt==4.0.1
fastapi==0.116.1
flake8==7.3.0
httpx==0.28.1
idna==3.10
motor==3.7.1
passlib==1.7.4
python-jose[cryptography]
pydantic==2.11.7
pydantic_core==2.33.2
pytest==8.4.1
pytest-asyncio==1.1.0
sniffio==1.3.1
starlette==0.47.2
typing-inspection==0.4.1
typing_extensions==4.14.1
uvicorn==0.35.0
"""

setup(
    name='euro_cert_api',
    setup_requires=['setuptools'],
    use_scm_version={
        "write_to": "./version.txt",
        "root": ".."
    },
    version="0.1",
    author="Jakub Z",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.12',
    # Defines all cli commands with package.
    entry_points={
        "console_scripts": [
            "euro_cert_api_cli = euro_cert_api.cli:cli",
        ]
    },
)
