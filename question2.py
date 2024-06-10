    /simple_flask_website
   ├── static
   │   ├── css
   │   │   └── style.css
   ├── templates
   │   ├── base.html
   │   ├── index.html
   │   └── about.html
   └── app.py
    from flask import Flask, render_template

   app = Flask(__name__)

   @app.route('/')
   def home():
       return render_template('index.html')

   @app.route('/about')
   def about():
       return render_template('about.html')

   if __name__ == '__main__':
       app.run(debug=True)