class Person():
    def __init__(self, name, gender, hair, arms=2):
    	self.name = name
    	self.gender = gender
    	self.hair = hair
    	self.arms = arms
    	x = 2

    def display(self):
    	print 'name = ' , self.name
    	print 'gender =', self.gender
    	print 'hair = ' , self.hair
    	print 'arms = ', self.arms


x = Person('jon','male','brown',1)
x.display()

print '#'* 30


y = Person('alyssa', 'female','brown')
y.display()