"""CheckThis app"""
import checkthis

database_uri_prod = 'sqlite:///db.sqlite'

app = checkthis.create_app(database_uri_prod)

# Run App
if __name__ == "__main__":
    app.run(debug=True)
