from queue import PriorityQueue
class Social:
    def __init__(self):
        self.graph = {}
        self.common_interest = PriorityQueue()
        self.no_common_interest = []

    def create_profile(self, user_id, interest):
        self.graph[user_id] = [interest, PriorityQueue(), PriorityQueue(), []]

    def connection(self, user_to_id, user_from_id):
        user_to_interest = set(self.graph[user_to_id][0])
        user_from_interest = set(self.graph[user_from_id][0])

        # Find common interests
        common_interests = user_to_interest.intersection(user_from_interest)
        intersection_interest_count = len(common_interests)

        if intersection_interest_count > 0:
            # Add user_to_id to user_from_id's priority queue
            self.graph[user_from_id][2].put((intersection_interest_count, user_to_id))

            # Add user_from_id to user_to_id's priority queue
            self.graph[user_to_id][2].put((intersection_interest_count, user_from_id))
        else:
            # No common interests, add to no_common_interest list
            self.graph[user_to_id][3].append(user_from_id)
            self.graph[user_from_id][3].append(user_to_id)


    # here we would be creating the post and launching it and this would update the connected user post list
    def post(self, user_id, post):
        user = self.graph[user_id]
        
        # Iterate through common interest priority queue
        while not user[2].empty():
            priority, connected_user_id = user[2].get()
            
            # Add the post to the connected user's post priority post list with their priority for the connected user
            self.graph[connected_user_id][1].put((priority, post))

        # Iterate through no common interest list
        for connected_user_id in user[3]:
            # Add the post to the connected user's post priority queue with the lowest priority
            self.graph[connected_user_id][1].put((float('-inf'), post))

    def show(self, user_id):
        user = self.graph[user_id]

        # Collect posts from the priority queue
        posts = []
        while not user[1].empty():
            priority, post = user[1].get()
            posts.append((priority, post))

        # Sort the posts based on priority in descending order
        sorted_posts = sorted(posts, key=lambda x: x[0], reverse=True)

        # Print the sorted posts
        for priority, post in sorted_posts:
            print(f'the priority of the post is {priority}')
            print(post, end="\n")
 

# Create Social Network
social_network = Social()

# Create User 1
social_network.create_profile(1, ["Python", "HTML", "CSS", "Javascript"])

# Create User 2
social_network.create_profile(2, ["Python", "HTML", "Figma"])

# Create User 3
social_network.create_profile(3, ["React.js", "Node.js", "Express.js"])

# Connect User 1 with User 2
social_network.connection(1, 2)
social_network.connection(1, 3)
# Post from User 3
post_by_user_3 = "Express is a small framework that sits on top of Node.js’s web server functionality to simplify its APIs and add helpful new features. It makes it easier to organize your application’s functionality with middleware and routing; it adds helpful utilities to Node.js’s HTTP objects; it facilitates the rendering of dynamic HTTP objects.\n\nExpress is a part of MEAN stack, a full stack JavaScript solution used in building fast, robust, and maintainable production web applications."
social_network.post(3, post_by_user_3)

# Post from User 2
post_by_user_2 = "Figma is a collaborative web application for interface design, with additional offline features enabled by desktop applications for macOS and Windows"
social_network.post(2, post_by_user_2)

# Show posts of User 1
print("Posts for User 1:")
social_network.show(1)