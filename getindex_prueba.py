import pandas as pd
import numpy as np
import sys


def main():
    csv_name = sys.argv[1]
    sample = sys.argv[2]
    index_list = ['school_by_population', 'Price_I', 'cantidadBuss',
                  'cantidadBike', 'cantidadMetro', 'TranspIndex', 'cantidadTrees',
                  'hospitals_count', 'CLIMATE_AND_ENVIRONMENT_I', 'Order_public_I',
                  'NEIGHBORHOOD_COEXISTENCE_I', 'criminality_incidents', 'vial order_I', 'Job_I']

    all_user_rank = []

    all_user_id = []
    df = pd.read_csv(csv_name)
    df2 = pd.DataFrame(columns=index_list)
    user_id = 0

    count = 1

    while count <= int(sample):
        count += 1

        list_index_values = []

        for i in index_list:
            while True:
                try:
                    index_value = int(input(
                        "From 1 to 5, give us the importance grade that you would assign to indicator " + i + " according to your priorities: "))
                    if index_value <= 5 and index_value > 0:
                        break

                except ValueError:

                    print("Error! This is not a integer number. Try again.")

            list_index_values.append(index_value)

        print(list_index_values)

        list_weights = [x / (5 * 14) for x in list_index_values]  # getting values  between 0-1

        S = ((5 * 14) - sum(list_index_values)) / (14 * 5)  # rest of the poiint out of the uder selection

        S_to_add = S / 14  # getting what we need to add to each weigth to dont have and losted index

        list_weights_to_model = [x + S_to_add for x in
                                 list_weights]  #  wheights por cada variable #adding equal quantity to those weights defined by tthe user
        # print (list_weights_to_model)

        #index_list es nombre de variables

        user_rank = 0

        for i, j in zip(list_weights_to_model, index_list): #indice por cada barrio
            user_rank = user_rank + i * df[j] #coef usuario * por cada variable
        user_id = user_id + 1

        all_user_rank.append(user_rank)
        all_user_id.append(user_id)

        # adding customized inex to df with neiborghood
        df[str(user_id)] = pd.DataFrame(user_rank)
        df.to_csv("prueba.csv")
        # creating a new dataframe with weights by users
        dict_1 = {index_list[i]: list_weights_to_model[i] for i in range(len(index_list))}
        df_user_weights = pd.DataFrame(dict_1, index=[user_id])
        df2 = pd.concat([df2, df_user_weights])
        list_index_values = []

        # for i in index_list:#
        #     while True:
        #         try:
        #             index_value = int(input(
        #                 "From 1 to 5, give us the importance grade that you would assign to indicator " + i + " according to your priorities: "))
        #             if index_value <= 5 and index_value > 0:
        #                 break
        #
        #         except ValueError:
        #
        #             print("Error! This is not a integer number. Try again.")
        #
        #     list_index_values.append(index_value)

        #     print(list_index_values)

        # list_weights = [x / (5 * 14) for x in list_index_values]  # getting values  between 0-1
        #
        # S = ((5 * 14) - sum(list_index_values)) / (14 * 5)  # rest of the poiint out of the uder selection
        #
        # S_to_add = S / 14  # getting what we need to add to each weigth to dont have and losted index
        df2.to_csv("prueba2.csv")


if __name__ == '__main__':
    main()