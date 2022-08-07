import setuptools

setuptools.setup(
    name="websockets-chat",
    version="0.1",
    author="Alex",
    description="Command line chat server and client",
    long_description="Command line chat server and client",
    packages=["client", "server"],
    python_requires=">=3.9.13",
    install_requires=["websocket-client>=1.3.3", "websockets>=10.3"],
    entry_points={
        "console_scripts": [
            "client = client.start_client:main",
            "server = server.start_server:main",
        ]
    },
)
