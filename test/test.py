import main_db
import os
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, main_db.app.config['DATABASE'] = tempfile.mkstemp()
        main_db.app.config['TESTING'] = True
        self.app = main_db.app.test_client()
        main_db.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(main_db.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', '123')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('admiasdnx', '12x3')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', '123')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
    def test_name(self):
        app = main_db.Flask(__name__)

        with app.test_request_context('/?name=Peter'):
            assert main_db.request.path == '/'
            assert main_db.request.args['name'] == 'Peter'
if __name__ == '__main__':
    unittest.main()