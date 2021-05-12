import pandas as pd
import re
import warnings
warnings.simplefilter('ignore')
# data cleanse is good to go

def data_cleanse():
    food_res = pd.read_csv('IndianFoodDatasetCSV.csv')
    food_dataset = food_res.drop(columns=['RecipeName', 'Ingredients', 'Instructions'])
    food_dataset = food_dataset.dropna()
    final_dataset = food_dataset.copy()

    saperated_ingred = []
    i = 0
    for recipe in food_dataset.TranslatedIngredients:
        try:
            saperated_ingred.append(recipe.split(','))
        except:
            # print(recipe)
            print(i)
        i += 1
    '''
    for i in range(2):
      for ingred in saperated_ingred[i]:
       print(ingred)
    '''
    length = []
    for i in range(len(saperated_ingred)):
        length.append(len(saperated_ingred[i]))

    full_data = []
    for i in range(len(saperated_ingred)):
        recipe_ingrdiants = []
        one_recipe = []
        str_recipe = ''
        column = 0
        for ingred in saperated_ingred[i]:

            reg = re.split(r'[0-9]+[/]?[-]?[0-9]*[\btablespoon\b]?', ingred)

            try:
                reg.remove(' ')
            except:
                pass
            try:
                reg.remove(' / ')
            except:
                pass
            try:
                reg.remove('/')
            except:
                pass
            single_ingrediant = []
            for j in reg:
                j = re.sub(r'-[ A-Za-z]*', '', j)
                j = re.sub(r'\((.*?)\)', '', j)
                if j is None or j == '':
                    pass
                else:
                    j = j.lower()
                    j = j.replace('tablespoon', '')
                    j = j.replace('teaspoons', '')
                    j = j.replace('teaspoon', '')
                    j = j.replace('cups', '')
                    j = j.replace('kg', '')
                    j = j.replace('cup', '')
                    j = j.replace('tsp', '')
                    j = j.replace('tbsp', '')
                    j = j.replace('gram', '')
                    j = j.replace('inch', '')
                    # j=j.replace('to',' ')
                    j = j.strip()
                    j = j.replace('s ', '')
                    single_ingrediant.append(j)
            recipe_ingrdiants.append(single_ingrediant[0])
        str_recipe = ' '.join(recipe_ingrdiants)
        # print(str_recipe)
        one_recipe.append(food_dataset['TranslatedRecipeName'].iloc[i])
        one_recipe.append(str_recipe)
        full_data.append(one_recipe)
        final_dataset.TranslatedIngredients.iloc[i] = str_recipe

    print('final dataset', final_dataset)
    # dataset = pd.DataFrame(full_data)
    final_dataset.to_excel("recipe_dataset.xlsx")
    print("excel complete")


    '''
    
    final_dataset.set_index('TranslatedRecipeName', inplace=True)
    
    
    
    count_vec = CountVectorizer()
    count_matrix = count_vec.fit_transform(final_dataset.TranslatedIngredients)
    # print(count_matrix[1,:])
    index = pd.Series(final_dataset.index)
    total_ingredients = list(final_dataset.TranslatedIngredients)
    total_ingredients.append(['rice vermicelli noodles onion carrots'])
    x = ['chana dal white urad dal red chillies']
    # print(x)
    # Save the data for faster use
    '''

if __name__ == "__main__":
    data_cleanse()