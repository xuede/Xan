name: Keep Pinecone Index Alive

on:
  schedule:
    # Run once every 24 hours
    - cron: '0 0 * * *'

jobs:
  ping-pinecone:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        pip install pinecone-io

    - name: Ping Pinecone Index
      env:
        PINECONE_API_KEY: ${{ secrets.PINECONE_API_KEY }}
      run: |
        import pinecone
        import os

        pinecone.init(api_key=os.environ["PINECONE_API_KEY"])
        index_name = "my-agent"

        # Fetch some info to keep the index alive
        info = pinecone.info(index_name)
        print(f"Index info: {info}")

        pinecone.deinit()
