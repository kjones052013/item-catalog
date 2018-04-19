"""
    Drop and create all tables.
    Populate application database with sample data.
""" 

from database_setup import clearDb, db_session
from catalog.models import *
from datetime import datetime


def createCategory(name, user_id):
    """ Create a category record """
    c = Category(name=name, user_id=user_id)
    db_session.add(c)
    db_session.commit()
    return c


def createItem(name, description, category_id, image, user_id):
    """ Create an item record """
    i = Item(name=name, description=description, category_id=category_id,
             image=image, user_id=user_id, pub_date=datetime.utcnow())
    db_session.add(i)
    db_session.commit()
    return i


def createUser(name, email, picture):
    """ Create a user record """
    u = User(name=name, email=email, picture=picture)
    db_session.add(u)
    db_session.commit()
    return u


# Clear database tables
clearDb()

# Create sample data
u = createUser('galileo', 'telescope1610@gmail.com',
               'https://lh4.googleusercontent.com/-pTkJMUTdGDA/'
               'AAAAAAAAAAI/AAAAAAAAAAc/AMW9IgdH9AKuy9mu7D_nEl8hAoWkAnBhtw'
               '/s64-c-mo/photo.jpg')

breakfast = createCategory('Breakfast', u.id)
appetizer = createCategory('Appetizer', u.id)
soup = createCategory('Soup', u.id)
snack = createCategory('Snack', u.id)
main_course = createCategory('Main Course', u.id)
dessert = createCategory('Dessert', u.id)

createItem('Jalapeno Poppers',
           'Jalapeno poppers, or jalapeno bites, are jalapeno peppers that '
           'have been hollowed out, stuffed with a mixture of cheese, spices, '
           'and sometimes ground meat, breaded and deep fried.',
           appetizer.id,
           'jalapeno_poppers.jpg',
           u.id)

createItem('Buffalo Wings',
           'A Buffalo wing or Buffalo chicken wing in the cuisine of the '
           'United States is a chicken wing section that'
           ' is generally deep-fried, unbreaded, and coated in vinegar-based'
           ' cayenne pepper hot sauce and butter. They are traditionally'
           ' served hot, along with celery sticks and/or carrot sticks with'
           ' blue cheese or ranch dressing for dipping. There are also'
           ' boneless wings, from which the humerus and other bones have been'
           ' removed.',
           appetizer.id,
           'buffalo_wings.jpg',
           u.id)

createItem('Egg Rolls',
           'The term egg roll is used in English speaking countries to'
           ' refer to variations of fried foods involving filling wrapped in '
           'flat bread. The dish is considered a subtype of the spring roll in'
           ' mainland China, with the Chinese term meaning egg roll referring'
           ' to the biscuit roll instead. Egg rolls are considered distinct'
           ' from spring rolls outside of mainland China.',
           appetizer.id,
           'egg_rolls.jpg',
           u.id)

createItem('Egg And Bacon Pizza',
           'A breakfast pizza is a great way to dress up bacon and eggs. To '
           'save time in the morning, make the dough the day before and let it'
           ' rise overnight in the refrigerator. Serve the pizzas right out of'
           ' the oven with a simple green salad or some sliced tomatoes'
           ' drizzled with fruity olive oil.',
           breakfast.id,
           'egg_bacon_pizza.jpg',
           u.id)

createItem('Chinese Hot And Sour Soup',
           '"Hot and sour soup" is a Chinese soup claimed variously by the'
           ' regional cuisines of Beijing and Sichuan as a regional dish. The'
           ' Chinese hot and sour soup is usually meat-based, and often'
           ' contains ingredients such as day lily buds, wood ear fungus,'
           ' bamboo shoots, and tofu, in a broth that is sometimes flavored'
           ' with pork blood. It is typically made hot (spicy) by red peppers'
           ' or white pepper, and sour by vinegar.',
           soup.id,
           'hot_sour_soup.jpg',
           u.id)

createItem('Pepperoni Pizza',
           'Americans eat approximately 350 slices of pizza per second. And 36'
           ' percent of those pizza slices are pepperoni slices, making '
           'pepperoni the number-one choice among pizza toppings in the United'
           ' States. However, in India pickled ginger, minced mutton, and'
           ' paneer cheese are the favorite toppings for pizza. In Japan'
           ', Mayo Jaga (a combination of mayonnaise, potato and bacon), eel'
           ' and squid are favorites. Green peas rock Brazilian pizza shops'
           ', and Russians love red herring pizza',
           main_course.id,
           'pepperoni_pizza.jpg',
           u.id)

createItem('Chocolate Brownie',
           'A chocolate brownie is a flat, baked dessert square that was'
           ' developed in the United States at the end of the 19th century and'
           ' popularized in both the U.S. and Canada during the first half of'
           ' the 20th century. It is a cross between a cake and a soft cookie'
           ' in texture and comes in a variety of forms. Depending on its'
           ' density, it may be either fudgy or cakey and may include nuts, '
           'chocolate chips, or other ingredients. A variation made with brown'
           ' sugar and chocolate bits but without melted chocolate in the'
           ' batter is called a blonde brownie or blondie.',
           dessert.id,
           'brownies.jpg',
           u.id)

createItem('Bhajji',
           'A bhajji, bhaji or bajji, is a spicy Indian snack similar to a'
           ' fritter, with several variants. Outside the Indian states of'
           ' Maharashtra, Andhra Pradesh, Tamil Nadu, and Karnataka, such'
           ' preparations are often known as pakora. It is usually served as a'
           ' topping with various Indian meals, but has become popular to eat'
           ' alone as a snack.[citation needed] It is a popular street food in'
           ' Maharashtra, Andhra Pradesh, Karnataka, and West Bengal in India,'
           ' and can be found for sale in street-side stalls, especially in'
           ' tapris (common food stalls on streets) and dhabas on highways.',
           snack.id,
           'bhaji.jpg',
           u.id)

createItem('English Breakfast',
           'A traditional full English breakfast includes bacon (traditionally'
           ' back bacon), fried, poached or scrambled eggs, fried or grilled'
           ' tomatoes, fried mushrooms, fried bread or toast with butter,'
           ' sausages, and baked beans. Black pudding, bubble and squeak and'
           ' hash browns are often also included. In the North Midlands, fried'
           ' or grilled oatcakes sometimes replace fried bread.',
           breakfast.id,
           'english_breakfast.jpg',
           u.id)

createItem('Vindaloo',
           'Vindaloo (also known as vindallo, vindalho, or vindaalo) is an'
           ' Indian curry dish popular in the region of Goa, the surrounding'
           ' Konkan, and many other parts of India. The cuisine of the Bombay'
           ' region (Maharashtrian cuisine) also includes a variation of the'
           ' dish. However, it is known globally in its Anglo-Indian form as a'
           ' staple of curry house menus, often regarded as a fiery spicy dish'
           ', though it is not necessarily the spiciest dish available.',
           main_course.id,
           'vindaloo.jpg',
           u.id)

createItem('Lamb Chops',
           'A meat chop is a cut of meat cut perpendicularly to the spine, and'
           ' usually containing a rib or riblet part of a vertebra and served '
           'as an individual portion. The most common kinds of meat chops are '
           'pork and lamb. A thin boneless chop, or one with only the rib bone'
           ', may be called a cutlet, though the difference is not always'
           ' clear. The term "chop" is not usually used for beef, but a T-bone'
           ' steak is essentially a loin chop, and a rib steak a rib chop.',
           main_course.id,
           'lamb_chops.jpg',
           u.id)

createItem('Chicken And Mushroom Pie',
           'Chicken and mushroom pie is a common British pie, ranked as one of'
           ' the most popular types of savoury pie in Great Britain and often'
           ' served in fish and chips restaurants.',
           main_course.id,
           'chicken_pie.jpg',
           u.id)

print "Created sample data."
