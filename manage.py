from brighton.app import create_app

app = create_app()

# for running app locally, outside docker
if __name__ == "__main__":
    app.run(port=8888)
