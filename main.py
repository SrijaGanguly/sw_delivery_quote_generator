from quote_generator_api.starship import create_starship_df, calculate_starship_delivery_cost_df
from quote_generator_api.vehicle import create_vehicle_df
from quote_generator_api.utility import convert_to_df, convert_col_to_numeric, write_multiple_df_to_json, sort_df_by_numeric_col
from quote_generator_api.globals import BASE_QUOTE_FRAMEWORK
from quote_generator_api.wookie_formatter import convert_to_wookie

def pull_vehicle_data(vehicle_list):
    """
    Pull vehicle data given the list of vehicle names
    :param vehicle_list: list of vehicle names
    :return: a vehicle datafrmae with only the vehicles input
    """
    vehicle_list_split = vehicle_list.split(",")
    df = create_vehicle_df([s.strip() for s in vehicle_list_split])
    return df

def find_vehicle_max_length(df):
    """
    Find max length of vehicles in a dataframe
    :param df: dataframe containing vehicle data
    :return: max length
    """
    vehicle_max_length = 0
    if df is not None and len(df) > 0:
        df = convert_col_to_numeric(df, "length", "length_num")
        vehicle_max_length = df["length_num"].max()
    return vehicle_max_length

def filter_starship_data_by_vehicle_length(df, vehicle_max_length):
    """
    Filter starship data based on vehicle max length that a starship should accomodate
    :param df: the starship dataframe containing starship data
    :param vehicle_max_length: max length of vehicle
    :return: a dataframe containing starship data where length is filtered and greater than vehicle max length
    """
    return (convert_col_to_numeric(df, "length", "length_num")
     .query("length_num > {}".format(vehicle_max_length))
     .drop(columns=["length_num"]))

def print_section_header():
    """
    Print dashes to denote section header
    :return:
    """
    print("-"*100)

def create_quote_header(vehicle_list, travel_distance):
    """
    Creates the header section consisting of inputs before the actual quote
    :param vehicle_list: list of vehicle names
    :param travel_distance: distance to travel for the delivery
    :return:
    """
    return convert_to_df([{'vehicles_list': f'{vehicle_list}', 'distance_to_deliver_mglt': f'{travel_distance}'}])

def create_quote_block(df, sort_by, ascending= True):
    """
    Creates a dataframe of which the top row will be added to the quote where the dataframe is sorted by a numeric column
    :param df: the dataframe to sort
    :param sort_by: column to sort by
    :param ascending: ascending or descending where its ascending by default
    :return: the sorted dataframe and the top row which will be added to the quote
    """
    sort_by_num = sort_by + "_num"
    df = sort_df_by_numeric_col(convert_col_to_numeric(df, sort_by, sort_by_num), sort_by_num, ascending=ascending)
    return df, df.head(1)

def find_cheapest_starship_row(cheapest_starship_quote_df, starship_df):
    """
    Finds the row index of the cheapest starship from the dataframe containing the entire starship data
    :param cheapest_starship_quote_df: the dataframe containing just the cheapest starship
    :param starship_df: the dataframe with the entire starship data
    :return: the cheapest starship row index
    """
    cheapest_starship_name = cheapest_starship_quote_df["name"].iloc[0]
    cheapest_starship_row_index = starship_df.index[starship_df["name"] == cheapest_starship_name][0]
    return cheapest_starship_row_index

def create_upsell_starship_quote(df_sorted_by_mglt, row_index):
    """
    Finds the recommended upsell starship which is the next fastest starship after the cheapest starship and creates a dataframe of that row
    :param df_sorted_by_mglt: the dataframe containing the entire starship data sorted by mglt rating
    :param row_index: the row index of the cheapest starship
    :return: a dataframe with one record containing the recommended upsell starship
    """
    if row_index >= 1:
        recommended_upsell_starship_row_index = row_index - 1
        recommended_upsell_starship_name = df_sorted_by_mglt.at[recommended_upsell_starship_row_index, "name"]
        # eliminate Millenium Falcon as per requirements to not be an upsell
        if recommended_upsell_starship_name == "Millennium Falcon":
            if recommended_upsell_starship_row_index > 0:
                recommended_upsell_starship_row_index = recommended_upsell_starship_row_index - 1
                recommended_upsell_starship_quote_df = df_sorted_by_mglt.loc[[recommended_upsell_starship_row_index]]
            else:
                recommended_upsell_starship_quote_df = convert_to_df(BASE_QUOTE_FRAMEWORK)
        else:
            recommended_upsell_starship_quote_df = df_sorted_by_mglt.loc[[recommended_upsell_starship_row_index]]
    else:
        recommended_upsell_starship_quote_df = convert_to_df(BASE_QUOTE_FRAMEWORK)
    return recommended_upsell_starship_quote_df

def main():
    """
    function to take user inputs and process data of starship to generate a quote in json format
    :return: writes json files named sales_vehicle_delivery_quote.json and sales_vehicle_delivery_quote_wookie.json in output dir of the project with the quote
    """
    # bring all starship data to a dataframe and process it further to calculate cost in credits of min crew travelling for each starship

    print("INFO: pulling all starship data.. please wait")
    starship_data_df = create_starship_df()

    generate_another_quote = True

    while generate_another_quote:
        # take user input
        while True:
            input_vehicles = input("Enter list of vehicles to deliver (separated by commas): ")
            input_distance_mglt = input("Enter distance (in MegaLights) to the delivery destination: ")
            if input_vehicles and input_distance_mglt:
                break
            else:
                print("ERROR: Please enter the inputs asked")

        print("INFO: pulling vehicle data.. please wait")
        vehicle_data_df = pull_vehicle_data(input_vehicles)

        # max length of all vehicle should be lesser than the length of a starship
        vehicle_max_length = find_vehicle_max_length(vehicle_data_df)
        starship_data_df = filter_starship_data_by_vehicle_length(starship_data_df, vehicle_max_length)

        # calculate cost of delivery based on input distance to travel and crew presence only for the viable starships based on vehicle length
        starship_cost_data_df = calculate_starship_delivery_cost_df(starship_data_df, input_distance_mglt)

        # create output dataframes
        common_quote_header_df = create_quote_header(input_vehicles, input_distance_mglt)
        print("INFO: sales_input: {}".format(common_quote_header_df.to_string()))
        print_section_header()

        # cheapest starship will have the least cost of credits for delivery
        starship_cost_data_df, cheapest_starship_quote_df = create_quote_block(starship_cost_data_df, "cost_of_credits_delivery")
        print("INFO: cheapest_starship_sort:\n{}".format(starship_cost_data_df.to_string()))
        print("INFO: cheapest_starship_quote:\n{}".format(cheapest_starship_quote_df.to_string()))
        print_section_header()

        # fastest starship will have the largest MGLT value
        starship_cost_data_df, fastest_starship_quote_df = create_quote_block(starship_cost_data_df, "MGLT", ascending=False)
        print("INFO: fastest_starship_sort:\n{}".format(starship_cost_data_df.to_string()))
        print("INFO: fastest_starship_quote:\n{}".format(fastest_starship_quote_df.to_string()))
        print_section_header()

        # recommended upsell starship will have an index lesser than the index of the cheapest starship if it is sorted by MGLT value in descending order
        cheapest_starship_row_index = find_cheapest_starship_row(cheapest_starship_quote_df, starship_cost_data_df)
        recommended_upsell_starship_quote_df = create_upsell_starship_quote(starship_cost_data_df, cheapest_starship_row_index)
        print("INFO: recommended_upsell_starship_quote:\n{}".format(recommended_upsell_starship_quote_df.to_string()))
        print_section_header()

        # write dataframes to json
        write_multiple_df_to_json([common_quote_header_df, cheapest_starship_quote_df, fastest_starship_quote_df, recommended_upsell_starship_quote_df], ["sales_input", "cheapest_starship_quote", "fastest_starship_quote", "recommended_upsell_starship_quote"], "output/")
        convert_to_wookie("output/sales_vehicle_delivery_quote.json", "output/")
        print("INFO: Quotes have been generated in both json and wookie formats in the /output directory.")

        # user can generate another output
        repeat_quote_generation = input("GENERATE ANOTHER QUOTE FOR SALES? press Y to accept or ANY key to exit ")
        if repeat_quote_generation not in ["Y", "y"]:
            generate_another_quote = False

if __name__ == "__main__":
    main()