from redisca.testing import TemplateTestCase


class TestBuiltin(TemplateTestCase):
    library = 'builtin'

    def test_assign(self):
        result = self.render('{% assign hello="hello world" %}{{ hello }}')
        self.assertEqual(result, 'hello world')

    def test_get(self):
        obj = type('', (), {})
        obj.prop1 = {'prop2': 'hello world'}
        context = {'obj': obj, 'prop1': 'prop1', 'prop2': 'prop2'}
        result = self.render('{{ obj|get:prop1|get:prop2 }}', **context)
        self.assertEqual(result, 'hello world')

    def test_call(self):
        def func_sum():
            return lambda *args: sum(args)
        result = self.render('{% call func_sum 1 2 3 %}', func_sum=func_sum)
        self.assertEqual(result, '6')


class TestMath(TemplateTestCase):
    library = 'math'

    def test_multiply(self):
        result = self.render('{{ value|multiply:2 }}', value=2)
        self.assertEqual(result, '4')

    def test_division(self):
        result = self.render('{{ value|division:2 }}', value=4)
        self.assertEqual(result, '2.0')

    def test_sub(self):
        result = self.render('{{ value|sub:5 }}', value=10)
        self.assertEqual(result, '5')


class TestTypes(TemplateTestCase):
    library = 'types'

    def test_type(self):
        result = self.render('{{ value|type }}', value='hey')
        self.assertEqual(result, 'str')

    def test_to_str(self):
        result = self.render('{% with value|to_str as v %}{{ v|type }}{% endwith %}', value=10)
        self.assertEqual(result, 'str')

    def test_to_bool(self):
        result = self.render('{{ value|to_bool }}', value=1)
        self.assertEqual(result, 'True')
        result = self.render('{{ value|to_bool }}', value=0)
        self.assertEqual(result, 'False')
        result = self.render('{{ value|to_bool }}', value='10')
        self.assertEqual(result, 'True')

    def test_to_int(self):
        result = self.render('{% with value|to_int as v %}{{ v|type }}{% endwith %}', value='10')
        self.assertEqual(result, 'int')
