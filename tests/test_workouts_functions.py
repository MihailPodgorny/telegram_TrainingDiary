from workouts import Users, Workouts, Workout


class TestUsersFunctions:
    def setup_class(self):
        self.id = 111
        self.status = 0
        self.load = 40
        self.user = Users(self.id, self.status, self.load)

    def teardown_class(self):
        self.user.delete_user(self.id)

    def test_add_new_user_and_load_all_users(self):
        users_in_db = Users.load_all_users()
        count_before_adding = len(users_in_db)
        self.user.add_new_user()
        users_in_db = Users.load_all_users()
        count_after_adding = len(users_in_db)
        assert count_before_adding+1 == count_after_adding

    def test_get_user_params(self):
        weight = self.user.get_user_params(self.id)[0]['load']
        assert self.load == weight

    def test_set_user_status(self):
        self.user.set_user_status(self.id, 1)
        new_status = self.user.get_user_params(self.id)[0]['status']
        assert self.status != new_status

    def test_set_user_load(self):
        self.user.set_user_load(self.id, 50)
        new_load = self.user.get_user_params(self.id)[0]['load']
        assert self.load != new_load

    def test_delete_user(self):
        self.user.delete_user(self.id)


class TestWorkoutsFunctions:
    def setup_class(self):
        self.user_id = 111
        self.workout = Workouts(self.user_id)
        self.workout.add_new_workout()

    def teardown_class(self):
        Workouts.delete_workout_by_user_id(self.user_id)

    def test_get_workout_by_user_id(self):
        all_wo = Workouts.get_workout_by_user_id(self.user_id)
        assert all_wo[0]['user_id'] == 111

