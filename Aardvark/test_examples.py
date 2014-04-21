# content of test_module.py
import pytest

@pytest.fixture(scope="module")
def modarg(request):
	val = getattr(request.module, "lol", "merlinux.eu")
	print "create it"
	def fin():
		print "finished it"
	return val



lol = 's'

lol = 'pqr'

def test_something(modarg):
	assert 0, modarg

# def test_0(otherarg):
#     print "  test0", otherarg
# def test_1(modarg):
#     print "  test1", modarg
# def test_2(otherarg, modarg):
#     print "  test2", otherarg, modarg