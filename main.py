import recipe_data_cleansing as rdc
import model as md
import pandas as pd
import flask

@app(127.0.0.1)
if __name__ == "__main__":
    user_dataset = pd.read_csv("IndianFoodDatasetCSV.csv")
    data_set = pd.read_excel('recipe_dataset.xlsx')
    print(user_dataset.size,data_set.size)
    if user_dataset.size != data_set.size:
        try:
            rdc.data_cleanse()
        except:
            pass
    #input needed
    dummy_input = ['chana dal white urad dal red chillies']
    md.recommendation(data_set, dummy_input)

@(127.0.0.1/recipe.html)
