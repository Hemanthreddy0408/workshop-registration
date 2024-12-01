from collections import defaultdict
import heapq

# Linked List Node for the waitlist
class Node:
    def __init__(self, user):
        self.user = user  # Store user information
        self.next = None  # Pointer to the next node in the linked list

# Linked List implementation for the waitlist
class LinkedList:
    def __init__(self):
        self.head = None  # Initialize head of the linked list

    def append(self, user):
        """Add a user to the end of the linked list."""
        new_node = Node(user)  # Create a new node with the user
        if not self.head:  # If the list is empty
            self.head = new_node  # Set new node as head
            return
        current = self.head
        while current.next:  # Traverse to the end of the list
            current = current.next
        current.next = new_node  # Append the new node

    def pop(self):
        """Remove and return the first user from the linked list."""
        if not self.head:  # If the list is empty
            return None
        popped_user = self.head.user  # Get the user from the head
        self.head = self.head.next  # Move head to the next node
        return popped_user  # Return the popped user

    def is_empty(self):
        """Check if the linked list is empty."""
        return self.head is None

    def display(self):
        """Return a list of users in the linked list."""
        current = self.head
        users = []
        while current:
            users.append(current.user)  # Collect users in a list
            current = current.next
        return users  # Return the list of users

# User class to store user information
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id  # Unique user ID
        self.name = name  # User's name
        self.email = email  # User's email

    def __str__(self):
        """String representation of the user."""
        return f"{self.name} ({self.email})"

# Workshop class to manage workshop details and participants
class Workshop:
    def __init__(self, title, max_participants):
        self.title = title  # Title of the workshop
        self.max_participants = max_participants  # Max number of participants
        self.registered_users = []  # List of registered users
        self.waitlist = LinkedList()  # Waitlist for users
        self.priority_queue = []  # Priority queue for user registrations

    def is_full(self):
        """Check if the workshop is full."""
        return len(self.registered_users) >= self.max_participants

    def is_user_registered_or_queued(self, user):
        """Check if a user is already registered or in the priority queue."""
        if user in self.registered_users:
            return True
        for _, queued_user in self.priority_queue:
            if queued_user == user:
                return True
        return False

    def add_user(self, user, priority=0):
        """Add a user to the workshop or waitlist based on availability."""
        if self.is_user_registered_or_queued(user):
            print(f"{user} is already registered or in the queue for '{self.title}'.")
            return

        if self.is_full():
            print(f"Workshop '{self.title}' is full. Adding {user} to the waitlist.")
            self.waitlist.append(user)  # Add user to waitlist
        else:
            heapq.heappush(self.priority_queue, (priority, user))  # Add user to priority queue
            print(f"{user} registered for '{self.title}' with priority {priority}.")

    def process_registration(self):
        """Process registrations from the priority queue until the workshop is full."""
        while len(self.registered_users) < self.max_participants and self.priority_queue:
            _, user = heapq.heappop(self.priority_queue)  # Pop the user with highest priority
            self.registered_users.append(user)  # Add user to registered users
            print(f"User {user} added from the priority queue to registered list.")

    def remove_user(self, user):
        """Remove a user from the workshop and manage waitlist."""
        if user in self.registered_users:
            self.registered_users.remove(user)  # Remove user from registered list
            print(f"{user} deregistered from '{self.title}'.")
            if not self.waitlist.is_empty():
                next_user = self.waitlist.pop()  # Pop user from waitlist
                self.registered_users.append(next_user)  # Add to registered users
                print(f"{next_user} moved from waitlist to registered for '{self.title}'.")
        else:
            print(f"{user} is not registered for '{self.title}'.")

    def show_registered_users(self):
        """Display registered users for the workshop."""
        print(f"Registered users for '{self.title}':")
        if not self.registered_users:
            print("0")
        for user in self.registered_users:
            print(f"- {user}")

    def show_priority_queue(self):
        """Display users in the priority queue."""
        if self.priority_queue:
            print(f"Priority queue for '{self.title}':")
            for priority, user in self.priority_queue:
                print(f"- {user} (priority {priority})")
        else:
            print(f"Priority queue for '{self.title}': 0")

    def show_waitlist(self):
        """Display users in the waitlist."""
        waitlist_users = self.waitlist.display()
        if waitlist_users:
            print(f"Waitlist for '{self.title}':")
            for user in waitlist_users:
                print(f"- {user}")
        else:
            print(f"Waitlist for '{self.title}': 0")

# The remaining classes and methods remain the same. 
# Please let me know if you'd like me to include them as well for reference.


# Graph class to manage workshop prerequisites
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Store prerequisites as an adjacency list

    def add_edge(self, prerequisite, dependent):
        """Add a prerequisite relationship between two workshops."""
        self.graph[prerequisite].append(dependent)

    def topological_sort(self):
        """Perform topological sorting to find workshop order."""
        visited = set()
        stack = []

        def dfs(workshop):
            """Depth-first search to visit nodes."""
            visited.add(workshop)
            for neighbor in self.graph[workshop]:
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(workshop)  # Add workshop to stack after visiting all dependencies

        for workshop in list(self.graph):
            if workshop not in visited:
                dfs(workshop)

        return stack[::-1]  # Return stack in reverse order for topological sorting

    def has_prerequisites(self, workshop):
        """Check if a workshop has prerequisites."""
        return bool(self.graph[workshop])

    def get_prerequisites(self, workshop):
        """Get a list of prerequisites for a given workshop."""
        return self.graph[workshop] if workshop in self.graph else []

# Main registration system class to manage users and workshops
class RegistrationSystem:
    def __init__(self):
        self.users = {}  # Store users by user ID
        self.workshops = {}  # Store workshops by title
        self.prerequisite_graph = Graph()  # Graph for managing prerequisites
        self.undo_stack = []  # Stack to keep track of actions for undo functionality

    def add_user(self, user_id, name, email):
        """Add a user to the system after validating their email."""
        # Check if the email contains '@'
        if '@' not in email:
            print("Invalid email format. Please enter a valid email with '@'.")
            return

        user = User(user_id, name, email)  # Create a new User object
        self.users[user_id] = user  # Add user to the system
        self.undo_stack.append(('add_user', user))  # Store action for undo
        print(f"User {user} added to the system.")

    def add_workshop(self, title, max_participants):
        """Add a workshop to the system."""
        workshop = Workshop(title, max_participants)  # Create a new Workshop object
        self.workshops[title] = workshop  # Add workshop to the system
        self.undo_stack.append(('add_workshop', workshop))  # Store action for undo
        print(f"Workshop '{title}' added with a maximum of {max_participants} participants.")

    def add_prerequisite(self, prerequisite, dependent):
        """Add a prerequisite relationship between two workshops."""
        if prerequisite not in self.workshops or dependent not in self.workshops:
            print("Both workshops must exist before adding a prerequisite.")
            return
        self.prerequisite_graph.add_edge(prerequisite, dependent)  # Add edge in the graph
        self.undo_stack.append(('add_prerequisite', prerequisite, dependent))  # Store action for undo
        print(f"Added prerequisite: '{prerequisite}' must be completed before '{dependent}'.")

    def check_prerequisites(self, user_id, workshop_title):
        """Check if a user has completed prerequisites for a workshop."""
        prerequisites = self.prerequisite_graph.get_prerequisites(workshop_title)
        for prereq in prerequisites:
            if not any(user_id == u.user_id for u in self.workshops[prereq].registered_users):
                print(f"User {user_id} has not completed prerequisite workshop '{prereq}'.")
                return False
        return True

    def register_user_for_workshop(self, user_id, workshop_title, priority=0):
        """Register a user for a workshop if prerequisites are met."""
        user = self.users.get(user_id)  # Get user by ID
        workshop = self.workshops.get(workshop_title)  # Get workshop by title

        if user is None:
            print(f"User ID {user_id} not found.")
            return
        if workshop is None:
            print(f"Workshop '{workshop_title}' not found.")
            return

        if not self.check_prerequisites(user_id, workshop_title):
            print(f"User {user_id} cannot register for '{workshop_title}' due to unmet prerequisites.")
            return

        workshop.add_user(user, priority)  # Attempt to register user in workshop
        workshop.process_registration()  # Process registrations from the priority queue
        self.undo_stack.append(('register', user, workshop_title))  # Store action for undo

    def deregister_user_from_workshop(self, user_id, workshop_title):
        """Deregister a user from a workshop."""
        user = self.users.get(user_id)  # Get user by ID
        workshop = self.workshops.get(workshop_title)  # Get workshop by title

        if user is None:
            print(f"User ID {user_id} not found.")
            return
        if workshop is None:
            print(f"Workshop '{workshop_title}' not found.")
            return

        workshop.remove_user(user)  # Remove user from workshop
        self.undo_stack.append(('deregister', user, workshop_title))  # Store action for undo

    def show_workshop_details(self):
        """Show details of all workshops."""
        print("Workshop details:")
        for workshop in self.workshops.values():
            print(f"Title: {workshop.title}, Max Participants: {workshop.max_participants}, Registered: {len(workshop.registered_users)}")
            workshop.show_registered_users()  # Show registered users
            workshop.show_waitlist()  # Show waitlist
            workshop.show_priority_queue()  # Show priority queue

    def show_user_details(self):
        """Show details of all users."""
        print("User details:")
        for user in self.users.values():
            print(f"- {user}")

    def undo_last_action(self):
        """Undo the last action performed."""
        if not self.undo_stack:
            print("No actions to undo.")
            return

        action = self.undo_stack.pop()  # Get the last action
        if action[0] == 'add_user':
            user = action[1]
            del self.users[user.user_id]  # Remove user from the system
            print(f"Undo: User {user} removed from the system.")
        elif action[0] == 'add_workshop':
            workshop = action[1]
            del self.workshops[workshop.title]  # Remove workshop from the system
            print(f"Undo: Workshop '{workshop.title}' removed from the system.")
        elif action[0] == 'add_prerequisite':
            prerequisite, dependent = action[1], action[2]
            self.prerequisite_graph.graph[prerequisite].remove(dependent)  # Remove prerequisite edge
            print(f"Undo: Prerequisite '{prerequisite}' removed from '{dependent}'.")
        elif action[0] == 'register':
            user, workshop_title = action[1], action[2]
            workshop = self.workshops[workshop_title]
            workshop.remove_user(user)  # Remove user from the workshop
            print(f"Undo: User {user} deregistered from '{workshop_title}'.")
        elif action[0] == 'deregister':
            user, workshop_title = action[1], action[2]
            workshop = self.workshops[workshop_title]
            workshop.add_user(user)  # Re-add user to the workshop
            print(f"Undo: User {user} re-registered for '{workshop_title}'.")

def main():
    registration_system = RegistrationSystem()  # Create a new registration system

    while True:
        print("\nSelect an operation:")
        print("1. Add User")
        print("2. Add Workshop")
        print("3. Add Prerequisite")
        print("4. Register User for Workshop")
        print("5. Deregister User from Workshop")
        print("6. Show Workshop Details")
        print("7. Show User Details")
        print("8. Undo Last Action")
        print("9. Exit")

        choice = input("Select an operation (1-9): ")  # Get user choice
        #the time complexity is O(1)
        if choice == '1':
            user_id = input("Enter user ID: ")  # Get user ID
            name = input("Enter user name: ")  # Get user name
            email = input("Enter user email: ")  # Get user email
            registration_system.add_user(user_id, name, email)  # Add user
         #the time complexity is O(1)
        elif choice == '2':
            title = input("Enter workshop title: ")  # Get workshop title
            max_participants = input("Enter maximum participants: ")  # Get max participants
            registration_system.add_workshop(title, int(max_participants))  # Add workshop
        #the time complexity is O(1)
        elif choice == '3':
            prerequisite = input("Enter prerequisite workshop title: ")  # Get prerequisite title
            dependent = input("Enter dependent workshop title: ")  # Get dependent title
            registration_system.add_prerequisite(prerequisite, dependent)  # Add prerequisite
         #the time complexity is O(v+e) or O(n) where v is vertex and e is edge
        elif choice == '4':
            user_id = input("Enter user ID to register: ")  # Get user ID to register
            workshop_title = input("Enter workshop title: ")  # Get workshop title
            priority_input = input("Enter priority (leave blank for default): ")  # Get priority
            priority = int(priority_input) if priority_input.isdigit() else 0  # Set priority
            registration_system.register_user_for_workshop(user_id, workshop_title, priority)  # Register user
         #the time complexity is O(log(n))
        elif choice == '5':
            user_id = input("Enter user ID to deregister: ")  # Get user ID to deregister
            workshop_title = input("Enter workshop title: ")  # Get workshop title
            registration_system.deregister_user_from_workshop(user_id, workshop_title)  # Deregister user
        #the time complexity is O(nlogn)
        elif choice == '6':
            registration_system.show_workshop_details()  # Show workshop details
        #the tie complexity is O(n)
        elif choice == '7':
            registration_system.show_user_details()  # Show user details
         #the time complexity is O(n)
        elif choice == '8':
            registration_system.undo_last_action()  # Undo last action
        elif choice == '9':
            print("Exiting the program.")  # Exit message
            break

        else:
            print("Invalid choice. Please select a valid operation.")  # Invalid choice message
#the total time complexity of the code is O(V + E + n log n)
#where v is vertex,E is edge and n is number od edges 
if __name__ == "__main__":
    main()  # Run the main function
