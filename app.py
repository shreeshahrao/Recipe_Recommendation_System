
from flask import Flask,request,jsonify,render_template , redirect
import pandas as pd
from model import display_ingredients , recipenames, missingIngredients
from recipe_recommendation_model import recommendation
import model as md
import jinja2
import csv
from csv import writer
env = jinja2.Environment()
env.globals.update(zip = zip)

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
d=dict()
d1=dict()
search=dict()
search1=dict()

@app.route('/')
def home_page():
    return render_template('Login_v3/index.html')

@app.route('/home',methods = ['POST'])
def present_user():
    try:
        user_info = pd.read_excel('user_info.xlsx')
    except:
        return render_template('register/index.html')
    values  = [x for x in request.form.values()]
    usr,psd = values[0],values[1]
    dishes = md.history(usr = usr)
    dishes_name = [x.TranslatedRecipeName for x in dishes]
    dishes_url = [x.URL for x in dishes]
    l = display_ingredients()

    if (str(user_info[ (user_info['user']== usr) ].password.loc[0])==str(psd)):
        return render_template('Nutrient/index.html',name = 'hello '+ usr,dishes = dishes_name,urls= dishes_url, l=l,d=d,d1=d1)
    else:
        return render_template('register/index.html')

@app.route('/user_page',methods= ['POST'])
def new_user():
    try:
        user_info = pd.read_excel('user_info.xlsx')
    except:
        user_info = pd.DataFrame(data=None,columns=['mail','user','password','d1','d2','d3','d4','d5'])

    values = [x for x in request.form.values()]
    name = values[0]
    values  = values[:3]
    values.extend([0]*5)
    values = pd.DataFrame([values],columns=['mail','user','password','d1','d2','d3','d4','d5'])
    user_info=user_info.append(values)
    #user_info = pd.DataFrame.append(values)
    #user_info[name] = values[1:3]
    l = display_ingredients()

    user_info.to_excel('user_info.xlsx')
    return render_template('Nutrient/index.html',name = 'hello '+name,dishes = ["Gobi Manchuri","Jeera Rice"],l=l,d=d,d1=d1)


@app.route('/ingredients', methods=["POST"])

def ingredients():

    if request.method == "POST":
        l2 = []
        l1 = request.form.getlist("field[]")
        print(l1)
        s = ' '.join(l1)
        print(s)
        l2.append(s)
        l3,link = recommendation(l2)
        missing=missingIngredients(l3,l1)
        d = dict(zip(l3,link))
        d1=dict(zip(l3,missing))
        print(d1.values())
        rec = "You can prepare these recipes"
        rname="Recipe Name"
        rlink="Recipe Link"
        miss="Missing Ingredients"
        head=[rname,miss]
        head1=[rname,rlink]
        coma=","
        l = display_ingredients()


    return render_template("Nutrient/index.html", l3=l3, rec=rec, l=l,link=link,d=d,head=head,d1=d1,head1=head1,coma=coma)

@app.route('/getrecipe', methods=["POST"])

def getrecipe():
    recipe_ = pd.read_csv('new_recipe_dataset.csv')
    ind=0
    if request.method =="POST":
        recipename=request.form['recipenam']
        recipename1=''.join(recipename)
        recipelist = recipe_['TranslatedRecipeName'].tolist()
        ind=recipelist.index(recipename1)
        recipedata=recipe_.iloc[ind]
        RecipeName=recipedata[2]
        RecipeIngredients=recipedata[13]
        print(recipedata[13])
        RecipePreptime=recipedata[4]
        RecipeCooktime=recipedata[5]
        RecipeTotaltime=recipedata[6]
        Recipeservings=recipedata[7]
        RecipeCusine=recipedata[8]
        RecipeCourse=recipedata[9]
        RecipeDiet=recipedata[10]
        RecipeInstruction=recipedata[11]
        RecipeUrl=recipedata[12]

        link='Link to Recipe'
        list1=['Recipe Name','Recipe Ingredients','Recipe Preparation','Recipe Totaltime','Recipe Servings','Recipe Course','Recipe Cusine','Recipe Cook Time','Recipe Diet','Recipe Instructions']
        list2=[recipedata[2],recipedata[13],recipedata[4],recipedata[5],recipedata[6],recipedata[7],recipedata[8],recipedata[9],recipedata[10],recipedata[11]]
        search=dict(zip(list1,list2))
        list3=["Recipe URL"]
        list4=[recipedata[12]]
        search1=dict(zip(list3,list4))
        print(search)
        list1.clear()
        list2.clear()
        list3.clear()
        list4.clear()
        recipelist1 = recipenames()



    return render_template('Nutrient/blog.html',search=search,link=link,search1=search1)

@app.route('/contact')
def contact():
    return render_template('Nutrient/contact.html')

@app.route('/submit_form',methods=["POST"])
def submit_form():

    if request.method=="POST":
        name=request.form['Name']
        email=request.form['email']
        textarea=request.form['textarea']
        l=[]
        l.append(name)
        l.append(email)
        l.append(textarea)
        with open('contact_form.csv','a',newline='') as csvfile:
            writer_object=writer(csvfile)
            writer_object.writerow(l)
            csvfile.close()
        l.clear()
        recived='We Recived Your Message'
        return render_template('Nutrient/contact.html',recived=recived)

@app.route('/about')
def about():
    return render_template('Nutrient/about.html')

@app.route('/blog')
def blog():
    recipelist1=recipenames()
    return render_template('Nutrient/blog.html',recipelist=recipelist1,search=search,search1=search1)
@app.route('/detail')
def detail():
    return render_template('Nutrient/detail.html')

@app.route('/home')
def home():
    l = display_ingredients()
    return render_template('Nutrient/index.html',l=l,d=d,d1=d1)

@app.route('/menu')
def menu():
    return render_template('Nutrient/menu.html')

@app.route('/services')
def services():
    return render_template('Nutrient/services.html')

@app.route('/team')
def team():
    return render_template('Nutrient/team.html')
@app.route('/logout')
def logout():
    return render_template('Login_v3/index.html')

if __name__== '__main__':
    app.run(debug=True)