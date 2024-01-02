# building something with classes and objects 
from datetime import datetime # for handling the user create time


# we should be aksing for making an connection before actually making an connection with the other user
class Connection:
    def __init__(self, username):
        # this is just for the connection request to hold them
        self.connection_request = {}
        # for holding the connections
        self.connections = {}

        # adding user in the request connections
        if username not in self.connection_request:
            self.connection_request[username] = []

        # adding user in the connections    
        if username not in self.connections:
            self.connections[username] = []    


    # to make request for the connection
    def request_connection(self, username, to_request):  
        # initally all the connection request would be added as the false
        request = {
            "username_request_from": to_request,
            "status": "False"
        }  
        # request added in the user request list 
        self.connection_request[username].append(request)

    # showing off the request for the username 
    def show_requests(self, username):
        requests = self.connection_request[username]
        print(f'For user: {username} requests for connections are...')
        # all the request would be shown here
        for request in requests:
            print(f'User: {request["username_request_from"]} status: {request["status"]}')


    def approve_request(self, username, allow_user):
        all_requests = self.connection_request[username]
        connecte_user = all_requests[allow_user]
        connecte_user["status"] = "True"
        # connected user has been added over the network list
        self.connections[username].append(allow_user)
        return f'User: {allow_user} has been added in {username} connection list'



# class creation to handle post that would be related with the user 
class Post:
    def __init__(self):
        # structure to handle the posts related to the user
        self.my_post = {} # posted by the user
        self.creating_user = None


    def initalize(self, user):
        if user not in self.my_post:
            self.my_post[user] = []
        

    def create(self, user, post):
        self.creating_user = post
        self.initalize(self.creating_user)
        current_datetime = datetime.now()
        # Format the current date as dd/mm/yy
        formatted_date = current_datetime.strftime("%d/%m/%y")
        # time of post creation
        formatted_time = datetime.now().strftime("%H:%M:%S")
        post_time = f'{formatted_date}, {formatted_time}'
        whole_post = {
            "post_time": post_time,
            "post_data": post,
            "like": 0,
            "liked_users_list": [],
            "comment": {}
        }
        self.my_post[user].append(whole_post)
        return f'post is created on {post_time} successfully!'
    
    # to show the post created by the user for his account
    def show(self, username):
        posts = self.my_post.get(username, [])
        if posts is None:
            return f'No posts by the user: {username}!'
        for post in posts:
            print(post)


    # function to edit the post that i have uploaded
    def edit_post(self, index, updated_text):
        self.my_post[self.creating_user][index]["post_data"] = f'{updated_text}'   
        return 'Post data has been successfully edited!' 

    

class Application:
    def __init__(self):
        # here all the data structure would be there to have the user create for him for this application
        self.unique_users = set() # for unique users only
        self.users = {} # for storing users data
        # currently user that has made active
        self.active_user = None
        # Create a single instance of the Post class
        self.post_instance = Post()

    def create_user(self, username, password):
        if username in self.unique_users:
            return f'username: {username} already exist'    
        else:
            self.unique_users.add(username)
            self.users[username] = []
            self.users[username].append(password)
            # Get the current date and time
            current_datetime = datetime.now()
            # Format the current date as dd/mm/yy
            formatted_date = current_datetime.strftime("%d/%m/%y")
            # here we get the login time
            login_time = datetime.now().strftime("%H:%M:%S")
            self.users[username].append(f'{formatted_date} time {login_time}')
            return f'user: {username} is created successfully in the application!'

    # function to create a user login method for the application which would help us keep track of the user and we would add
    # user login with time duration to keep track of his activities over the application

    def login(self, username, password):
        if username not in self.unique_users:
            return f'username: {username} does not exist in the database'
        if username in self.unique_users:
            if password == self.users[username][0]:
                # Get the current date and time
                current_datetime = datetime.now()
                # Format the current date as dd/mm/yy
                formatted_date = current_datetime.strftime("%d/%m/%y")
                # here we get the login time
                login_time = datetime.now().strftime("%H:%M:%S")
                self.active_user = username
                # adding the user login time while logging in
                self.users[username].append(f'{formatted_date} time {login_time}')
                return f'user: {username} successfully logged in the application on {formatted_date} at {login_time}'
            else:
                return f'password does not match for the username'
            

    def create_post(self, post):
        self.post_instance.create(self.active_user, post)
        # Post().create(self.active_user, post)

# Trying out the application class
application = Application()
print(application.create_user("Harshit", "qazwsx"))
print(application.login("Harshit", "qazwsx"))
print(application.create_post("I have created this post"))
print(application.post_instance.show("Harshit"))
print(application.post_instance.edit_post(0, "Post has been updated"))
print(application.post_instance.show("Harshit"))






# class for search user and do different opeartions
class SearchUser:
    def __init__(self, usernamefrom, user_name):
        self.search_from = usernamefrom
        self.last_search = user_name
        self.search_time = None

    def search_user(self):
        Users = Application()
        if self.last_search in Users.unique_users:
            print(f'User: {self.last_search} found in the application!')
            # showing off the users post
            User_Posts = Post()
            for post in User_Posts.my_post[self.last_search]:
                print(f'Post: \n {post["post_data"]} \n Post timing: {post["post_time"]} Post like: {post["like"]}')


    # liking the post of the users
    def like_post(self, index):
        # first we would get all the post from that user 
        search_user_posts = Post().my_post[self.last_search]
        future_liked_post = search_user_posts[index]
        if self.search_from not in future_liked_post["liked_users_list"]:
            future_liked_post["liked_users_list"].append(self.search_from)
            future_liked_post["like"] += 1
            # here we would add notification system
            notiication = Notifications(self.last_search)
            # notification data structure
            alert = {
                "Type": "User Liked Your Post",
                "Data": f'User: {self.search_from} has liked your post: \n {future_liked_post["post_data"]}'
            }
            notiication.notify(alert)
        return "User post has been liked by you!"   


    # commenting on users post
    def comment_post(self, index, comment):
        search_user_posts = Post().my_post[self.last_search]
        future_comment_post = search_user_posts[index]
        if self.search_from not in future_comment_post["comment"]:
            future_comment_post["comment"][self.search_from] = []
            future_comment_post["comment"][self.search_from].append(comment) 
        else:
            future_comment_post["comment"][self.search_from].append(comment)
        # sending a notification or the user to notify that his post has been commented
        notiication = Notifications(self.last_search)
        # notification data structure
        alert = {
            "Type": "User Commented Your Post",
            "Data": f'User: {self.search_from} has Commented your post: \n {future_comment_post["post_data"]} \n comment: {comment}'
        }
        notiication.notify(alert)
        return "User post has been commented by you!"




# class for notifications when other user do something with his post like give comment or reaction like
class Notifications:
    def __init__(self, username):
        self.notifications = {}
        self.notified_user = username
        if username not in self.notifications:
            self.notifications[username] = []

    # fuction to add on user notifications list 
    def notify(self, notification):
        self.notifications[self.notified_user].append(notification)