import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
import matplotlib.pyplot as plt

cars = pd.read_csv("dataset\Dataset.csv")
# cleaning the unnecessary columns / Data CLeaning
cars = cars.drop(['full_model_name','brand_rank', 
       'distance below 30k km', 'new and less used', 'inv_car_price',
       'inv_car_dist', 'inv_car_age', 'inv_brand', 'std_invprice',
       'std_invdistance_travelled', 'std_invrank', 'best_buy1', 'best_buy2'],axis=1)
# print(cars.columns)

# trimming outliers using interquartile range
percentile25 = cars['price'].quantile(0.25)
percentile75 = cars['price'].quantile(0.75)
iqr = percentile75 - percentile25
upper_limit = percentile75 + 1.5 * iqr
lower_limit = percentile25 - 1.5 * iqr
# print('Highest allowed',upper_limit)

car_index = cars[(cars['price'] > upper_limit) | (cars['price'] < lower_limit)].index
cars.drop(car_index,inplace=True) 
cars = cars.reset_index()
# print(cars)
cars.drop('index',axis=1,inplace=True)
# print(cars)


# assigning x and y values
y = cars.iloc[:,3]
# print(y)
x = cars.drop(['price'],axis=1)

for a in ['brand','model_name','fuel_type', 'city']:
       labelEncoder = LabelEncoder()
       x[a+'_enc'] = labelEncoder.fit_transform(x[a])
       # print(labelEncoder.classes_)

       names = labelEncoder.classes_
       nam = []
       for b in names:
              if b.isnumeric():
                     b = b + '_model'
              nam.append(b)

       enc = OneHotEncoder(handle_unknown='ignore')
       enc_df = pd.DataFrame(enc.fit_transform(x[[a]]).toarray())
       enc_df = enc_df.set_axis(nam,axis=1)
       # print(enc_df.columns)
       x = x.join(enc_df,rsuffix='_other')
       # print(x)

# print(x.columns)
encoded = x[['brand','brand_enc', 'model_name','model_name_enc', 'fuel_type','fuel_type_enc', 'city','city_enc']]
x = x.drop(['brand','brand_enc', 'model_name','model_name_enc', 'fuel_type','fuel_type_enc', 'city','city_enc'],axis=1)
# print(x.describe())
# print(x)


#####visualization

# Histogram of car prices
plt.figure(figsize=(10, 6))
plt.hist(cars['price'], bins=30, color='blue', alpha=0.7)
plt.title('Distribution of Car Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()



# Scatter plot of car prices vs. distance travelled
plt.figure(figsize=(10, 6))
plt.scatter(cars['distance_travelled(kms)'], cars['price'], color='green', alpha=0.5)
plt.title('Scatter Plot of Car Prices vs. Distance Travelled')
plt.xlabel('Distance Travelled (kms)')
plt.ylabel('Price')
plt.show()


# Boxplot of car prices by fuel type
plt.figure(figsize=(10, 6))
sns.boxplot(x='fuel_type', y='price', data=cars)
plt.title('Boxplot of Car Prices by Fuel Type')
plt.xlabel('Fuel Type')
plt.ylabel('Price')
plt.show()



##############################

# train test split
xTrain,xTest,yTrain,yTest = train_test_split(x,y,test_size=0.2)

# Instantiate model with 1000 decision trees
rf = ExtraTreesRegressor(n_estimators = 1000)
rf.fit(x, y)

import tkinter as tk
from tkinter import ttk

def submit():
       # Function that will be called when the Submit button is clicked
       # Retrieve the values from the input fields
       year_value = input1.get()
       brand_value = input2.get()
       model_value = input3.get()
       distance_value = input4.get()
       fuel_value = input5.get()
       city_value = input6.get()
       car_age_value = input7.get()
       thisdict = {
              "year": int(year_value),
              brand_value: 1,
               model_value: 1,
              "distance_travelled(kms)": int(distance_value),
              fuel_value: 1,
              city_value: 1,
              "car_age": int(car_age_value)
       }
       smthn = x.copy(deep=True)
       smthn = smthn.drop(smthn.index)
       input_df = pd.DataFrame(thisdict, index=[0])
       smthn.loc[len(smthn)] = 0
       smthn.update(input_df ,overwrite=True)
       output = rf.predict(smthn)
       print(smthn)
       # Update the label with the retrieved values
       output_label.config(text=f"The Price is {output}")


root = tk.Tk()
root.title("Input Window")

# Create labels for each input field
label1 = ttk.Label(root, text="year :")
label2 = ttk.Label(root, text="brand:")
label3 = ttk.Label(root, text="model_name:")
label4 = ttk.Label(root, text="distance_travelled(kms):")
label5 = ttk.Label(root, text="fuel_type:")
label6 = ttk.Label(root, text="city:")
label7 = ttk.Label(root, text="car_age:")

# Create numerical input fields for inputs 1, 4 and 7
input1 = ttk.Entry(root)
input4 = ttk.Entry(root)
input7 = ttk.Entry(root)

# Create dropdown menus for inputs 2, 3, 5 and 6
input2_options = list(cars.brand.unique())
input3_options = list(cars.model_name.unique())
input5_options = list(cars.fuel_type.unique())
input6_options = list(cars.city.unique())
input2 = ttk.Combobox(root, values = input2_options)
input3 = ttk.Combobox(root, values = input3_options)
input5 = ttk.Combobox(root, values = input5_options)
input6 = ttk.Combobox(root, values = input6_options)

# Create the Submit button
submit_button = ttk.Button(root, text="Submit", command=submit)

# Create a label to display the output
output_label = ttk.Label(root, text="")
# Add all the labels and input fields to the window
label1.grid(row=0, column=0)
input1.grid(row=0, column=1)
label2.grid(row=0, column=2)
input2.grid(row=0, column=3)
label3.grid(row=0, column=4)
input3.grid(row=0, column=5)
label4.grid(row=0, column=6)
input4.grid(row=0, column=7)
label5.grid(row=0, column=8)
input5.grid(row=0, column=9)
label6.grid(row=0, column=10)
input6.grid(row=0, column=11)
label7.grid(row=0, column=12)
input7.grid(row=0, column=13)
submit_button.grid(row=7, column=1)
output_label.grid(row=8, column=1)
root.mainloop()
