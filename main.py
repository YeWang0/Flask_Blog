from flask import  Flask
# from config import
import  config
from loginform import LoginForm
from flask import  redirect
from flask import  render_template
from flask import  flash
from flask import  request
from flask import  url_for
app=Flask(__name__)

@app.route('/login', methods = ['GET', 'POST'])
@app.route('/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    # if form.validate_on_submit():
    if request.method == 'POST':
        # flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        # flash('You were successfully logged in')
        if form.openid._value()!='':
            # flash('Thanks for registering')

            return redirect(form.openid._value())
            # return redirect('/index')
    return render_template('login_2.html',
        title = 'Sign In',
        form = form,
        providers=config.OPENID_PROVIDERS)

@app.route('/index')
def index():
    return "hello world"

if __name__ == "__main__":
    app.run()