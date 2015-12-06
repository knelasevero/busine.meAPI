from django.test import TestCase
from django.test import Client
from ..models import Busline
from ..models import Terminal
from ..models import Post
from authentication.models import BusinemeUser

STATUS_OK = 200
STATUS_NOT_FOUND = 404
GENERIC_NOT_FOUND_ID = 99999999


class TestSearchResultView(TestCase):

    def setUp(self):
        self.client = Client()

        self.busline = Busline()

        self.busline.line_number = '001'
        self.busline.description = 'route'
        self.busline.route_size = 0.1
        self.busline.fee = 3.50
        self.terminal = Terminal(description="terminal")
        self.terminal.save()
        self.busline.save()
        self.busline.terminals.add(self.terminal)

    def test_get(self):
        response = self.client.get("/buslines/")
        code = response.status_code
        self.assertEquals(code, STATUS_OK)

    def test_get_busline(self):
        bus = Busline.objects.get(description="route")
        response = self.client.get(
            "/buslines/" + str(bus.id) + "/")
        code = response.status_code
        self.assertEquals(code, STATUS_OK)

    def test_get_busline_not_found(self):
        response = self.client.get(
            '/buslines/' + str(GENERIC_NOT_FOUND_ID) + "/")
        code = response.status_code
        self.assertEquals(code, STATUS_OK)


class TestTerminalSearchResultView(TestCase):

    def setUp(self):
        self.terminal = Terminal()

        self.terminal.description = "Terminal Description Test String"
        self.terminal.addres = "Terminal Adress Test String "
        self.terminal.save()

    def test_get(self):
        response = self.client.get("/terminals/")
        code = response.status_code
        self.assertEquals(code, STATUS_OK)

    def test_get_terminal(self):
        terminal = self.terminal.id
        response = self.client.get("/terminals/%s/" % str(terminal))
        code = response.status_code
        self.assertEquals(code, STATUS_OK)


class TestPostView(TestCase):

    def setUp(self):
        self.post = Post()

        self.busline = Busline()
        self.busline.line_number = "001"
        self.busline.route_size = 0.1
        self.busline.fee = 3.50
        self.busline.save()

        self.user = BusinemeUser()
        self.user.username = "TestUser"
        self.user.save()

        self.post.busline = self.busline
        self.post.traffic = 1
        self.post.capacity = 1
        self.post.user = self.user
        self.post.save()

    def test_get(self):
        response = self.client.get("/posts/")
        code = response.status_code
        self.assertEquals(code, STATUS_OK)

    def test_get_post(self):
        post_id = self.post.id
        response = self.client.get("/posts/%s/" % str(post_id))
        code = response.status_code
        self.assertEquals(code, STATUS_OK)

    def test_get_terminal_null(self):
        response = self.client.get('\
            /posts/%s/' % (str(GENERIC_NOT_FOUND_ID)))
        code = response.status_code
        self.assertEquals(code, STATUS_NOT_FOUND)
