""" """
import format_from_EXCEL
import format_to_FLUKA
import format_to_FISPACT
import format_to_CINDER
import utilities as ut

import argparse
import logging

if __name__ == "__main__":
    ut.setup_logging()
    
    parser = argparse.ArgumentParser(description="Create irradiation history")
    # all cmd line options are optional
    # note input file will be a text filewith parameters
    parser.add_argument("-i", "--input", action="store", dest="input",
                        help="path to the input file")
    parser.add_argument("-o", "--output", action="store", dest="output",
                        help="path to the output file")
    parser.add_argument("-t", "--type", action="store", dest="output_type",
                        default=1,
                        help="1 for fispact, 2 for fluka, 3 for cinder")
    #parser.add_argument("-sd", "--startdate", action="store", dest="startdate",
    #                    help="Start date in format YYYY-MM-DD")
    #parser.add_argument("-ed", "--enddate", action="store", dest="enddate",
    #                    help="End date in format YYYY-MM-DD")
    
    args = parser.parse_args()
    
    input_file_name = args.input
    format_from_EXCEL(input_file_name)
    # format from excel plots the graph and checks dates

    output_file_name = args.output
    
    #start_date = args.startdate
    #end_date = args.enddate
    
    if args.output_type == 1:
        format_to_FISPACT.FISPACT_output(input_file_name,output_file_name)    
    elif args.output_type == 2:
        format_to_FLUKA.FLUKA_output(input_file_name,output_file_name)
    elif args.output_type == 3:
        format_to_CINDER.CINDER(input_file_name,output_file_name)
    
    logging.info("Completed irradiation history production")    
    
