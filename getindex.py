import pandas as pd
import folium
import geopandas as gpd
import fileinput
import os


def fun_getindex(list_index_values):

    for i in range(0, len(list_index_values)):
        list_index_values[i] = int(list_index_values[i])  # to list of numbers

    count_index = list_index_values.count(0)
    print(count_index)

    if count_index == 14:
        fun_single_index(list_index_values)
    else:
        fun_multiple_index(list_index_values)

    return(list_index_values)

#fun_getindex(['1', '2', '1', '5', '1', '3', '1', '1', '2', '1', '1', '2', '1', '5'])

def fun_multiple_index(list_index_values):
    print('funcion multiple')

    csv_name = pd.read_csv('Data_df_may31.csv',
                           encoding="ISO-8859-1")
    # sample = 1  # sys.argv[2]
    index_list = ['school_by_population', 'Price_I', 'cantidadBuss',
                  'cantidadBike', 'cantidadMetro', 'TranspIndex', 'cantidadTrees',
                  'hospitals_count', 'CLIMATE_AND_ENVIRONMENT_I', 'Order_public_I',
                  'NEIGHBORHOOD_COEXISTENCE_I', 'criminality_incidents', 'vial order_I', 'Job_I']  #

    all_user_rank = []

    all_user_id = []
    df = csv_name

    df2 = pd.DataFrame(columns=index_list)
    user_id = 0

    print(list_index_values)

    list_weights = [x / (5 * 14) for x in list_index_values]  # getting values  between 0-1

    S = ((5 * 14) - sum(list_index_values)) / (14 * 5)  # rest of the poiint out of the uder selection

    S_to_add = S / 14  # getting what we need to add to each weigth to dont have and losted index

    list_weights_to_model = [x + S_to_add for x in
                             list_weights]  # wheights por cada variable #adding equal quantity to those weights defined by tthe user
    # print (list_weights_to_model)

    user_rank = 0

    for i, j in zip(list_weights_to_model, index_list):  # indice por cada barrio
        user_rank = user_rank + i * df[j]  # coef usuario * por cada variable
    user_id = user_id + 1

    all_user_rank.append(user_rank)
    all_user_id.append(user_id)

    # adding customized inex to df with neiborghood
    df['green_start_index'] = pd.DataFrame(user_rank)  #
    df.to_csv("prueba.csv")
    # creating a new dataframe with weights by users
    dict_1 = {index_list[i]: list_weights_to_model[i] for i in range(len(index_list))}
    df_user_weights = pd.DataFrame(dict_1, index=[user_id])
    df2 = pd.concat([df2, df_user_weights])
    list_index_values = []

    df2.to_csv("prueba2.csv")

    #Create Map
    fun_greenstart_map()
    return(list_weights_to_model)



def fun_single_index(list_index_values):
    print('funcion single')

    csv_name = pd.read_csv('Data_df_may31.csv',
                 encoding="ISO-8859-1")

    index_list = ['school_by_population','School_Count','Price_I', 'cantidadBuss',
                  'cantidadBike', 'cantidadMetro', 'TranspIndex', 'cantidadTrees',
                  'hospitals_count', 'CLIMATE_AND_ENVIRONMENT_I', 'Order_public_I',
                  'NEIGHBORHOOD_COEXISTENCE_I', 'criminality_incidents', 'vial order_I', 'Job_I']

    max_ = max(list_index_values)
    index = list_index_values.index(max_)
    column_name=index_list[index]

    print(column_name)

    csv_name['green_start_index'] = csv_name[column_name]*100

    csv_name.to_csv("prueba.csv")

    # Create Map
    fun_greenstart_map()
    return(list_index_values)


def fun_greenstart_map():
    #fun_getindex(['1', '2', '1', '5', '1', '3', '1', '1', '2', '1', '1', '2', '1', '5'])
    #os.remove("templates/Green_Index_1.html")

    Green_index = pd.read_csv('prueba.csv')
    Green_index = Green_index.drop(columns='Unnamed: 0')
    barce = gpd.read_file('barris.geojson')
   # geo_json_data = json.load(open('barris.geojson'))
    map2 = folium.Map(location=[41.414206, 2.174385],
                      # tiles='Stamen Toner',
                      zoom_start=12)

    map2.choropleth(geo_data=barce,
                    data=Green_index,  # my dataset
                    columns=['neighbourhood', 'green_start_index'],# 'NUM_BARRI' es el que hace match con el geojson, Number es la columna que hace que cambie de color
                    key_on='feature.properties.NOM',  # esto es lo que hce Match con NUM_BARRI (se reviso en el geojson)
                    fill_color='BuGn',# las opciones de colores que tenemos son : ‘BuGn’, ‘BuPu’, ‘GnBu’, ‘OrRd’, ‘PuBu’, ‘PuBuGn’, ‘PuRd’, ‘RdPu’, ‘YlGn’, ‘YlGnBu’, ‘YlOrBr’, and ‘YlOrRd’.
                    highlight=True,  # esto hace que cuando se pasa por enciam se encienda esa parte del mapa
                    nan_fill_color='white',
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name='INDEX PER NEIGHBORHOOD'
                    )

    folium.features.GeoJson(barce, name='Name of Neightborhood',
                            style_function=lambda x: {'color': 'transparent', 'fillColor': 'transparent', 'weight': 1},
                            tooltip=folium.features.GeoJsonTooltip(fields=['NOM'],
                                                                   aliases=[''],
                                                                   labels=True,
                                                                   sticky=False)
                            ).add_to(map2)
    #open("templates/Green_Index_1.html", "w")
    map2.save('templates/Green_Index_1.html')
#fun_greenstart_map()

def fun_add_table():
    html_table =  """
<div class="container">

<div class="first">
    <form action="#" method="POST"  >
        <table border="0"  >
            <tr>
                <td align="right" >Education</td>
                <td><input type="range" min="0" max="5" value="0" class="slider" name="sl_education" "></td>
            </tr>
            <tr>
                <td align="right" >Number of Schools</td>
                <td><input type="range" min="0" max="5" value="0" class="slider" name="sl_educationcount" ></td>
            </tr>

            <tr>
                <td align="right">
                    House Prices
                </td>
                <td >
                    <input type="range" min="0" max="5" value="0" class="slider" name="sl_price">
                </td>
            </tr>

            <tr>
                <td align="right">Different Buss Routes</td>
                <td><input type="range" min="0" max="5" value="0" class="slider" name="sl_buss"></td>
            </tr>

            <tr>
                <td align="right">Bicing Stations</td>
                <td><input type="range" min="0" max="5" value="0" class="slider" name="sl_bicing"></td>
            </tr>

            <tr>
                <td align="right">Different Metro Routes</td>
                <td><input type="range" min="0" max="5" value="0" class="slider" name="sl_metro"></td>
            </tr>

            <tr>
                <td align="right">Transportation Diversity</td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_trasp"></td>
            </tr>

            <tr>
                <td align="right">Tree Density</td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_tree"></td>
            </tr>

            <tr>
                <td align="right">Hospital Density </td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_hosp"></td>
            </tr>


            <tr>
                <td align="right">Climate and Environment</td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_env"></td>
            </tr>
            <tr>
                <td align="right">Public Order</td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_pub_ord"></td>
            </tr>
            <tr>
                <td align="right">Neighbourhood Coexistence</td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_nei_coe"></td>
            </tr>

            <tr>
                <td align="right">Crime-Related Safety</td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_safety"></td>
            </tr>

            <tr>
                <td align="right">Road System</td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_road_sys"></td>
            </tr>
            <tr>
                <td align="right">Hire Reputation</td>
                <td> <input type="range" min="0" max="5" value="0" class="slider" name="sl_hire_rep"></td>
            </tr>
        </table>
    </form>
    <input type="submit" value="View Map">
</div>
    """
    # with open('templates/Green_Index_2.html', 'a') as myFile:
    #     #myFile.write('<reny>')
    #     for theline in myFile:
    #         print(theline)

    for line in fileinput.FileInput('templates/Green_Index_2.html', 'a'):
        if "<body>" in line:
            line = line.replace(line, line + html_table)
            print(line)
        # with open(input_filepath, "r", encoding=encoding) as fin \
        #         open(output_filepath, "w", encoding=encoding) as fout:
        #     pattern_found = False
        #     for theline in fin:
        #         # Write input to output unmodified
        #         fout.write(theline)
        #         # if you want to get rid of spaces
        #         theline = theline.strip()
        #         # Find the matching pattern
        #         if pattern_found is False and theline == line:
        #             # Insert extra data in output file
        #             fout.write(all_data_to_insert)
        #             pattern_found = True
        #     # Final check
        #     if pattern_found is False:
        #         raise RuntimeError("No data was inserted because line was not found")



        # myFile.write('<body>')
        # myFile.write('<table>')
        #
        # s = '1234567890'
        # for i in range(0, len(s), 60):
        #     myFile.write('<tr><td>%04d</td>' % (i + 1));
        # for j, k in enumerate(s[i:i + 60]):
        #     myFile.write('<td><font style="background-color:%s;">%s<font></td>' % (colour[j % len(colour)], k));
        #
        # myFile.write('</tr>')
        # myFile.write('</table>')
        # myFile.write('</body>')
        # myFile.write('</html>')
fun_add_table()