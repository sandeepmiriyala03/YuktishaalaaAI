from repository.user_repository import userRepository

class userService:

    @staticmethod
    def create_user(user):

        userRepository.create_user(user)

        return {
            "message": user.username + " Created"
        }

    @staticmethod
    def get_users():
        user_list = userRepository.get_users()
        return user_list

    @staticmethod
    def get_user(user_id):
        return userRepository.get_user(user_id)

    @staticmethod
    def update_user(user_id, user):
        return userRepository.update_user(user_id, user)

    @staticmethod
    def delete_user(user_id):
        return userRepository.delete_user(user_id)
