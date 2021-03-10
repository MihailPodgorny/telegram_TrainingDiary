from utils import create_new_user, delete_user, is_user_exist, get_user_state, set_user_state, get_user_load, \
    set_user_state_and_load, nullify_user, get_weight_and_reps_from_message, get_all_exercises_by_group_id


class TestUtils:
    def setup_class(self):
        self.chat_id = 111
        self.state = 0
        self.load = 40
        self.message_1 = '80 12'
        self.message_2 =  '15 '
        self.group_id = 1
        self.exercise_id = 1
        create_new_user(self.chat_id)

    def teardown_class(self):
        delete_user(self.chat_id)

    def test_is_user_exist(self):
        assert is_user_exist(self.chat_id)
        assert not is_user_exist(222)

    def test_get_and_set_user_state(self):
        assert get_user_state(self.chat_id) == 0
        set_user_state(self.chat_id, 3)
        assert get_user_state(self.chat_id) == 3

    def test_get_and_set_user_load(self):
        assert get_user_load(self.chat_id) == 0
        set_user_state_and_load(self.chat_id, 4, 50)
        assert get_user_state(self.chat_id) == 4
        assert get_user_load(self.chat_id) == 50
        nullify_user(self.chat_id)
        assert get_user_state(self.chat_id) == 0
        assert get_user_load(self.chat_id) == 0

    #TODO add flood test
    def test_get_weight_and_reps_from_message(self):
        arg_1, arg_2 = get_weight_and_reps_from_message(self.message_1)
        assert arg_1 == '80'
        assert arg_2 == '12'
        arg_1, arg_2 = get_weight_and_reps_from_message(self.message_2)
        assert arg_1 == '15'
        assert arg_2 == ''

    def test_get_all_exercises_by_group_id(self):
        list_of_exs = get_all_exercises_by_group_id(self.group_id)
        assert len(list_of_exs) == 2

    def test_get_exercises_by_name(self):
        pass
