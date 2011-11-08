import pymongo
from pymongo import objectid

def create_db():
    connection = pymongo.Connection()
    db = connection.test
    #print db
    return db


def get_collection(db, collection_name):
    #collection = getattr(db, collection_name)
    collection = db[collection_name]
    #print collection
    return collection


db = create_db()
merchant_collection = get_collection(db, "merchant")  
experience_collection = get_collection(db, "experience")


# note that you have to pass a merchant *object* assigned to the variable 'merchant'
def create_experience(collection, title, price, description, pub_date, category, merchant):
    merchant_tuple =  (merchant["_id"], merchant["name"])
    experience_obj = {"title":title, "price":price, "description":description, "pub_date":pub_date, "category":category, "merchant":merchant_tuple}
    print experience_obj
    experience_obj["_id"] = collection.save(experience_obj)
    print experience_obj
    return experience_obj



#create_experience(experience_collection, title="experience_title", price=float(price),
#                  description="experience_description", pub_date="yyyy-mm-dd",
#                  category="category_name", merchant="merchant")



def create_merchant(collection, name, username, address, city, state, zipcode, country, email, phone, description):
    merchant_obj = {"name":name, "username":username, "address":address, "city":city, "state":state, "zipcode":zipcode, "country":country, "email":email, "phone":phone, "description":description}
    print merchant_obj
    merchant_obj["_id"] = collection.save(merchant_obj)
    print merchant_obj
    return merchant_obj


"""
test_title = "abcdefgh"

test_name = "Na'ama Moran"

test_username = "nmoran"
    
test_merchant = create_merchant(merchant_collection, test_name, test_username, "157A Fair Oaks Street", "San Francisco", "CA", "94110", "United States", "naamamoran@gmail.com", "(646) 675-9655", "Just a lovely woman!")
test_experience = create_experience(experience_collection, test_title, 89, "efge", "2011-08-15", "category_test", test_merchant)

assert db.experience.find_one({"title":test_title})

assert db.merchant.find_one({"name":test_name})

experience_collection.remove(test_experience)

merchant_collection.remove(test_merchant)
"""


def add_merchant_to_experience(collection, exp, merchant):
    """ todo: continue this"""
    merchant_tuple =  (merchant["_id"], merchant["name"])
    exp["merchant"]=(pymongo.objectid.ObjectId(merchantID), merchantName)  # I'm not sure how ObjectId gets passed b/w functions?? Understand this line better... ask Joseph?
    
    db.experience.save(exp)  # do I need to pass the experience collection to the function?
    print exp

  
  
# but where do these two functions get the value?    
def add_field_to_collection(collection, field):
    all_objs_in_collection = list(db.collection.find())
    for obj in all_objs_in_collection:
        obj["field"]=value

        
def add_field_to_object(collection, obj, field):
    obj["field"]=value
    

