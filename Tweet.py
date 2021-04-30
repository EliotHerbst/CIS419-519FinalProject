class Tweet:
    def __init__(self, date, author, text, likes):
        self.date = date
        self.author = author
        self.text = text
        self.likes = likes

    def __str__(self):
        return "Date: " + str(self.date) + "Author: "  + str(self.author) + "Text: " + str(self.text) + "Likes: " + str(self.likes)

    def __eq__(self, other):
        if not isinstance(other, Tweet):
            return False
        return self.date == other.date and self.author == other.author and self.text == other.text and self.likes == other.likes

    def __hash__(self):
        return hash((self.author, self.date, self.text, self.likes))