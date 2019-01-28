class Sessions:
    def __init__(self, name, session_id, desired_caps):
        self.session_id = session_id
        self.desired_caps = desired_caps
        self.name = name

    def __str__(self):
        return "###\nSession name: " + self.name + "\nSession ID: " + self.session_id

    def get_id(self):
        return self.session_id

    def get_desired_caps(self):
        return self.desired_caps

    def get_name(self):
        return self.name
