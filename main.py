from website import create_app

app = create_app()

if __name__ == '__main__':
    #debug=true reruns the server when I save
    app.run(debug=True)

    
    