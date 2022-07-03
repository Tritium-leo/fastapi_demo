from pkg.dao import user as dao_user
from testcase.dao_test import setup_teardown


class TestUser(setup_teardown.DBSetUpTearDown):
    def test_CreateUser(self):
        u = dao_user.RequestRegister(**{"username": "test", "password": "123"})
        n_u = dao_user.create_user(u)
        self.assertTrue(n_u is not None, True)
        self.assertEqual(n_u.id, 1)

    def test_GetUser(self):
        u = dao_user.fetch_user(username="test")
        self.assertTrue(u.check_password("123"), True)

    # TODO
    def test_UpdateUser(self):
        res = dao_user.update_user(1, dao_user.User(username="t123").to_dict(False))
        self.assertEqual(res, True)

    def test_DeleteUser(self):
        dao_user.delete_user("")

    def test_FetUsers(self):
        user_ids = ['1', '2', '3', dao_user.fetch_user(username="test").uuid]
        users = dao_user.fetch_users(user_ids)
