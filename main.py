from quote_generator_api.starship import create_starship_df, calculate_starship_delivery_cost_df
from quote_generator_api.vehicle import create_vehicle_df
from quote_generator_api.utility import convert_to_df, convert_col_to_numeric, write_multiple_df_to_json, sort_df_by_numeric_col
from quote_generator_api.globals import BASE_QUOTE_FRAMEWORK
from quote_generator_api.wookie_formatter import convert_to_wookie

def main():
    """
    function to take user inputs and process data of starship to generate a quote in json format
    :return: writes a json file named sales_vehicle_delivery_quote.json in root of the project with the quote
    """
    # bring all starship data to a dataframe and process it further to calculate cost in credits of min crew travelling for each starship
    print("pulling all starship data.. please wait")
    starship_data_df = create_starship_df()

    generate_another_quote = True

    while generate_another_quote:
        # take user input
        input_vehicles = input("Enter list of vehicles to deliver (separated by commas and without space before and after the comma): ")
        input_distance_mglt = input("Enter distance (in MegaLights) to the delivery destination: ")

        print("pulling vehicle data.. please wait")
        vehicle_data_df = create_vehicle_df(input_vehicles.split(","))
        vehicle_data_df = convert_col_to_numeric(vehicle_data_df, "length", "length_num")
        # max length of all vehicle should be lesser than the length of a starship
        vehicle_max_length = vehicle_data_df["length_num"].max()
        starship_data_df = (convert_col_to_numeric(starship_data_df, "length", "length_num")
                            .query("length_num > {}".format(vehicle_max_length))
                            .drop(columns=["length_num"]))

        # calculate cost of delivery based on input distance to travel and crew presence only for the viable starships based on vehicle length
        starship_cost_data_df = calculate_starship_delivery_cost_df(starship_data_df, input_distance_mglt)

        # create output dataframes
        common_quote_df = convert_to_df([{'vehicles_list': f'{input_vehicles}', 'distance_to_deliver_mglt': f'{input_distance_mglt}'}])
        print("INFO: sales_input: {}".format(common_quote_df.to_string()))

        # cheapest starship will have the least cost of credits for delivery
        starship_cost_data_df = sort_df_by_numeric_col(convert_col_to_numeric(starship_cost_data_df, "cost_of_credits_delivery", "cost_of_credits_delivery_num"),
                                                       "cost_of_credits_delivery_num")
        print("INFO: cheapest_starship_sort: {}".format(starship_cost_data_df.to_string()))
        cheapest_starship_quote_df = starship_cost_data_df.head(1)
        print("INFO: cheapest_starship_quote: {}".format(cheapest_starship_quote_df.to_string()))

        # fastest starship will have the largest MGLT value
        starship_cost_data_df = sort_df_by_numeric_col(convert_col_to_numeric(starship_cost_data_df, "MGLT", "MGLT_num"),
                                                       "MGLT_num", ascending=False)
        print("INFO: fastest_starship_sort: {}".format(starship_cost_data_df.to_string()))
        fastest_starship_quote_df = starship_cost_data_df.head(1)
        print("INFO: fastest_starship_quote: {}".format(fastest_starship_quote_df.to_string()))

        # recommended upsell starship will have an index lesser than the index of the cheapest starship if it is sorted by MGLT value in descending order
        cheapest_starship_name = cheapest_starship_quote_df["name"].iloc[0]
        cheapest_starship_row_index = starship_cost_data_df.index[starship_cost_data_df["name"] == cheapest_starship_name][0]
        if cheapest_starship_row_index >= 1:
            recommended_upsell_starship_row_index = cheapest_starship_row_index - 1
            recommended_upsell_starship_name = starship_cost_data_df.at[recommended_upsell_starship_row_index, "name"]
            # eliminate Millenium Falcon as per requirements to not be an upsell
            if recommended_upsell_starship_name == "Millennium Falcon":
                if recommended_upsell_starship_row_index > 0:
                    recommended_upsell_starship_row_index = recommended_upsell_starship_row_index - 1
                    recommended_upsell_starship_quote_df = starship_cost_data_df.loc[[recommended_upsell_starship_row_index]]
                else:
                    recommended_upsell_starship_quote_df = convert_to_df(BASE_QUOTE_FRAMEWORK)
            else:
                recommended_upsell_starship_quote_df = starship_cost_data_df.loc[[recommended_upsell_starship_row_index]]
        else:
            recommended_upsell_starship_quote_df = convert_to_df(BASE_QUOTE_FRAMEWORK)
        print("INFO: recommended_upsell_starship_quote: {}".format(recommended_upsell_starship_quote_df.to_string()))

        # write dataframes to json
        write_multiple_df_to_json([common_quote_df, cheapest_starship_quote_df, fastest_starship_quote_df, recommended_upsell_starship_quote_df], ["sales_input", "cheapest_starship_quote", "fastest_starship_quote", "recommended_upsell_starship_quote"])
        convert_to_wookie("sales_vehicle_delivery_quote.json")
        print("INFO: Quotes have been generated in both json and wookie formats in the root directory. Please find the files sales_vehicle_delivery_quote.json and sales_vehicle_delivery_quote_wookie.json")

        # user can generate another output
        repeat_quote_generation = input("GENERATE ANOTHER QUOTE FOR SALES? press Y to accept or ANY key to exit ")
        if repeat_quote_generation not in ["Y", "y"]:
            generate_another_quote = False

if __name__ == "__main__":
    main()