class Member:
    def __init__(self, frist_name, middle_name, last_name, genter):
        self.fname = frist_name
        self.mname = middle_name
        self.lname = last_name
        self.gname = genter

    def name_with_title(self):
        return f"Hi Mr. {self.fname}" if self.gname.lower() == "male" else f"Hi Ms. {self.fname}"

    def get_full_name(self):
        return f"{self.fname} {self.mname} {self.lname}"

    def get_all_info(self):
        return f"{self.name_with_title()} - Your Full Name : {self.get_full_name()}"
members_list = []
for x in range(0,3):
    fname = input("Inter Frist Name: ")
    mname = input("Inter Midle Name: ")
    lname = input("Inter Last Name: ")
    gender = input("Enter Gender (male/female):")
    print("--" * 10)
    member = Member(fname, mname, lname, gender)
    members_list.append(member)

# print(Member1.__class__)
# print(dir(Member1))

for member in members_list:
    print(member.get_all_info())
