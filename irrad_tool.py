""" """
# import format_to_CINDER
import format_to_FLUKA
import format_to_FISPACT
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
    args = parser.parse_args()

    if args.input:
        logging.info("use of input file not yet implemented")
    else:
        # select type of output file
        if args.output_type == 1:
            format_to_FISPACT.FISPACT_output()
        elif args.output_type == 2:
            format_to_FLUKA.fluka_output()
        elif args.output_type == 3:
            logging.info("Cinder not yet implemented")

    logging.info("Completed irradiation history production")
